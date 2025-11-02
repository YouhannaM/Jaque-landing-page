"""
AI Training Pipeline for Quality Standards
Uses sentence transformers for document embeddings and similarity search
"""

import json
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime
import sqlite3


@dataclass
class DocumentEmbedding:
    """Document with embedding vector"""
    document_id: str
    text: str
    embedding: np.ndarray
    metadata: Dict


class QualityStandardsTrainer:
    """Train and use AI models for quality standards recommendations"""

    def __init__(self, db_path: str = "manufacturing.db"):
        self.db_path = db_path
        self.model = None
        self.embeddings_cache = {}

    def initialize_model(self):
        """Initialize the embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            # Use a lightweight but effective model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Loaded embedding model: all-MiniLM-L6-v2")
        except ImportError:
            print("⚠ sentence-transformers not installed. Using simple TF-IDF fallback.")
            self._initialize_tfidf_fallback()

    def _initialize_tfidf_fallback(self):
        """Fallback to TF-IDF if sentence-transformers not available"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.model = TfidfVectorizer(
            max_features=384,  # Match MiniLM dimension
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.is_tfidf = True
        print("✓ Using TF-IDF fallback model")

    def preprocess_document(self, text: str) -> str:
        """Preprocess document text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        if self.model is None:
            self.initialize_model()

        processed_text = self.preprocess_document(text)

        if hasattr(self, 'is_tfidf') and self.is_tfidf:
            # TF-IDF fallback
            return self.model.fit_transform([processed_text]).toarray()[0]
        else:
            # Sentence transformer
            return self.model.encode(processed_text, convert_to_numpy=True)

    def train_on_quality_standards(self):
        """Train embeddings on all quality standards in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all quality standards
        cursor.execute("""
            SELECT id, standard_id, title, full_text, summary, category, industry, applicable_processes
            FROM quality_standards
        """)

        standards = cursor.fetchall()
        print(f"\n📚 Training on {len(standards)} quality standards...")

        for standard in standards:
            std_id, standard_id, title, full_text, summary, category, industry, processes = standard

            # Combine relevant text for embedding
            combined_text = f"""
            Title: {title}
            Standard: {standard_id}
            Category: {category}
            Summary: {summary}
            Full Text: {full_text}
            """

            # Generate embedding
            embedding = self.generate_embedding(combined_text)

            # Store embedding back to database
            embedding_json = json.dumps(embedding.tolist())

            cursor.execute("""
                UPDATE quality_standards
                SET embedding_vector = ?
                WHERE id = ?
            """, (embedding_json, std_id))

            print(f"  ✓ Processed: {standard_id}")

        conn.commit()
        conn.close()
        print("✅ Training completed!\n")

    def find_relevant_standards(
        self,
        query: str,
        industry: str = None,
        top_k: int = 5
    ) -> List[Dict]:
        """Find most relevant quality standards for a query"""
        if self.model is None:
            self.initialize_model()

        # Generate query embedding
        query_embedding = self.generate_embedding(query)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build query with optional industry filter
        sql = "SELECT id, standard_id, title, summary, category, industry, embedding_vector FROM quality_standards"
        params = []

        if industry:
            sql += " WHERE json_extract(industry, '$') LIKE ?"
            params.append(f'%"{industry}"%')

        cursor.execute(sql, params)
        standards = cursor.fetchall()

        # Calculate similarities
        similarities = []
        for standard in standards:
            std_id, standard_id, title, summary, category, industries, embedding_json = standard

            if embedding_json:
                stored_embedding = np.array(json.loads(embedding_json))
                similarity = self.cosine_similarity(query_embedding, stored_embedding)

                similarities.append({
                    'standard_id': standard_id,
                    'title': title,
                    'summary': summary,
                    'category': category,
                    'industries': json.loads(industries) if industries else [],
                    'similarity': float(similarity)
                })

        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        conn.close()

        return similarities[:top_k]

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def generate_quality_plan_recommendations(
        self,
        part_description: str,
        material: str,
        industry: str,
        tolerances: List[Dict]
    ) -> Dict:
        """Generate quality plan recommendations using AI"""

        # Build query from part information
        query = f"""
        Manufacturing part: {part_description}
        Material: {material}
        Industry: {industry}
        Tolerances: {', '.join([f"{t.get('feature')}: ±{t.get('tolerance')}mm" for t in tolerances])}
        """

        # Find relevant standards
        relevant_standards = self.find_relevant_standards(query, industry=industry)

        # Get applicable quality plan template
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, description, inspection_points, control_methods,
                   acceptance_criteria, documentation_requirements
            FROM quality_plan_templates
            WHERE json_extract(industries, '$') LIKE ?
            ORDER BY
                CASE complexity_level
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    ELSE 4
                END
            LIMIT 1
        """, (f'%"{industry}"%',))

        template = cursor.fetchone()

        if not template:
            # Fallback to general template
            cursor.execute("""
                SELECT id, name, description, inspection_points, control_methods,
                       acceptance_criteria, documentation_requirements
                FROM quality_plan_templates
                LIMIT 1
            """)
            template = cursor.fetchone()

        conn.close()

        if not template:
            return {
                'error': 'No quality plan template available',
                'relevant_standards': relevant_standards
            }

        template_id, name, desc, inspection_points, control_methods, acceptance, docs = template

        # Build comprehensive quality plan
        quality_plan = {
            'template_used': name,
            'description': desc,
            'relevant_standards': relevant_standards,
            'inspection_points': json.loads(inspection_points),
            'control_methods': json.loads(control_methods),
            'acceptance_criteria': json.loads(acceptance),
            'documentation_requirements': json.loads(docs),
            'ai_recommendations': self._generate_ai_insights(
                part_description, material, tolerances, relevant_standards
            )
        }

        return quality_plan

    def _generate_ai_insights(
        self,
        part_description: str,
        material: str,
        tolerances: List[Dict],
        relevant_standards: List[Dict]
    ) -> List[str]:
        """Generate AI-powered insights for quality planning"""
        insights = []

        # Analyze tolerance requirements
        tight_tolerances = [t for t in tolerances if float(t.get('tolerance', 1)) < 0.01]
        if tight_tolerances:
            insights.append(
                f"Identified {len(tight_tolerances)} critical dimensions with tolerances < ±0.01mm. "
                f"Recommend CMM inspection with SPC monitoring."
            )

        # Material-based recommendations
        material_lower = material.lower()
        if 'titanium' in material_lower:
            insights.append(
                "Titanium material requires specialized tooling and cutting parameters. "
                "Monitor tool wear closely and validate process capability."
            )
        elif 'stainless' in material_lower:
            insights.append(
                "Stainless steel machining may cause work hardening. "
                "Control feed rates and monitor surface finish carefully."
            )

        # Standards-based recommendations
        for standard in relevant_standards[:2]:  # Top 2 most relevant
            if 'AS9100' in standard['standard_id']:
                insights.append(
                    f"Based on {standard['standard_id']}, require First Article Inspection (FAI) "
                    f"and maintain complete traceability."
                )
            elif 'ISO-13485' in standard['standard_id']:
                insights.append(
                    f"Medical device standard {standard['standard_id']} applies. "
                    f"Ensure process validation and full lot traceability."
                )
            elif 'IATF' in standard['standard_id']:
                insights.append(
                    f"Automotive standard {standard['standard_id']} requires PPAP submission "
                    f"and control plan with key characteristics identified."
                )

        return insights


class MachineRecommendationEngine:
    """AI engine for recommending machines based on part requirements"""

    def __init__(self, db_path: str = "manufacturing.db"):
        self.db_path = db_path

    def recommend_machines(
        self,
        part_dimensions: Dict[str, float],
        material: str,
        required_operations: List[str],
        annual_volume: int,
        tolerance: float
    ) -> List[Dict]:
        """Recommend machines based on part requirements"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get machines that can handle the material
        cursor.execute("""
            SELECT DISTINCT m.id, m.name, m.manufacturer, m.model, m.category,
                   m.price, m.max_part_size_x, m.max_part_size_y, m.max_part_size_z,
                   m.tolerance, m.repeatability, m.cycle_time_factor,
                   m.features, m.automation_level, m.lead_time_weeks
            FROM machines m
            JOIN machine_materials mm ON m.id = mm.machine_id
            JOIN materials mat ON mm.material_id = mat.id
            WHERE mat.name LIKE ?
            AND m.is_available = 1
        """, (f'%{material}%',))

        machines = cursor.fetchall()

        # Score each machine
        scored_machines = []

        for machine in machines:
            (m_id, name, manufacturer, model, category, price, max_x, max_y, max_z,
             mach_tolerance, repeatability, cycle_factor, features, automation, lead_time) = machine

            score = 0
            reasons = []

            # Check size compatibility
            if (part_dimensions.get('x', 0) <= max_x and
                part_dimensions.get('y', 0) <= max_y and
                part_dimensions.get('z', 0) <= max_z):
                score += 30
                reasons.append("✓ Sufficient work envelope")
            else:
                continue  # Skip if part doesn't fit

            # Check tolerance capability
            if mach_tolerance <= tolerance:
                score += 25
                reasons.append(f"✓ Meets tolerance requirement (±{tolerance}mm)")
            else:
                score -= 10
                reasons.append(f"⚠ Tolerance capability: ±{mach_tolerance}mm (required: ±{tolerance}mm)")

            # Volume considerations
            if annual_volume > 5000:
                if automation == 'FULLY_AUTO':
                    score += 20
                    reasons.append("✓ High automation for volume production")
                elif automation == 'SEMI_AUTO':
                    score += 10
            else:
                if automation == 'MANUAL' or automation == 'SEMI_AUTO':
                    score += 10
                    reasons.append("✓ Appropriate automation level for volume")

            # Cycle time efficiency
            if cycle_factor < 0.9:
                score += 15
                reasons.append(f"✓ Efficient cycle time (factor: {cycle_factor})")

            # Check capabilities match required operations
            cursor.execute("""
                SELECT c.name
                FROM capabilities c
                JOIN machine_capabilities mc ON c.id = mc.capability_id
                WHERE mc.machine_id = ?
            """, (m_id,))

            capabilities = [cap[0] for cap in cursor.fetchall()]
            matching_ops = sum(1 for op in required_operations if op in capabilities)

            if matching_ops == len(required_operations):
                score += 20
                reasons.append("✓ All required operations supported")
            elif matching_ops > 0:
                score += 10
                reasons.append(f"⚠ {matching_ops}/{len(required_operations)} operations supported")

            scored_machines.append({
                'id': m_id,
                'name': name,
                'manufacturer': manufacturer,
                'model': model,
                'category': category,
                'price': price,
                'tolerance': mach_tolerance,
                'automation_level': automation,
                'lead_time_weeks': lead_time,
                'features': json.loads(features) if features else {},
                'capabilities': capabilities,
                'score': score,
                'reasons': reasons
            })

        conn.close()

        # Sort by score
        scored_machines.sort(key=lambda x: x['score'], reverse=True)

        return scored_machines[:5]  # Return top 5


# Example usage
if __name__ == "__main__":
    print("🤖 Quality Standards AI Trainer\n")

    # Initialize trainer
    trainer = QualityStandardsTrainer()

    # Train on quality standards
    trainer.train_on_quality_standards()

    # Test recommendations
    print("\n🔍 Testing Quality Plan Generation...\n")
    quality_plan = trainer.generate_quality_plan_recommendations(
        part_description="Precision shaft with tight concentricity requirements",
        material="Aluminum 6061-T6",
        industry="aerospace",
        tolerances=[
            {'feature': 'diameter', 'tolerance': 0.005},
            {'feature': 'length', 'tolerance': 0.1},
            {'feature': 'concentricity', 'tolerance': 0.01}
        ]
    )

    print("Quality Plan Generated:")
    print(f"  Template: {quality_plan['template_used']}")
    print(f"  Relevant Standards: {len(quality_plan['relevant_standards'])}")
    for std in quality_plan['relevant_standards'][:3]:
        print(f"    - {std['standard_id']}: {std['title'][:60]}...")

    print(f"\n  AI Insights: {len(quality_plan['ai_recommendations'])}")
    for insight in quality_plan['ai_recommendations']:
        print(f"    • {insight}")

    # Test machine recommendations
    print("\n\n🔧 Testing Machine Recommendations...\n")
    engine = MachineRecommendationEngine()
    machines = engine.recommend_machines(
        part_dimensions={'x': 150, 'y': 50, 'z': 50},
        material='Aluminum 6061',
        required_operations=['TURNING', 'DRILLING'],
        annual_volume=10000,
        tolerance=0.005
    )

    print(f"Top {len(machines)} Recommended Machines:")
    for i, machine in enumerate(machines, 1):
        print(f"\n  {i}. {machine['name']} ({machine['manufacturer']})")
        print(f"     Score: {machine['score']}/100")
        print(f"     Price: ${machine['price']:,.0f}")
        print(f"     Tolerance: ±{machine['tolerance']}mm")
        for reason in machine['reasons']:
            print(f"     {reason}")

    print("\n✅ All tests completed!\n")
