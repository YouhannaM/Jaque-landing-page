"""
Seed database with sample machines, quality standards, and training data
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Machine, Capability, Material, QualityTool, QualityStandard, QualityPlanTemplate
from datetime import datetime
import json

# Database setup
DATABASE_URL = "sqlite:///manufacturing.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


def seed_capabilities():
    """Seed manufacturing capabilities"""
    session = SessionLocal()

    capabilities = [
        Capability(name="TURNING", category="MACHINING", description="Rotational cutting operations"),
        Capability(name="MILLING", category="MACHINING", description="Multi-axis cutting operations"),
        Capability(name="DRILLING", category="MACHINING", description="Hole making operations"),
        Capability(name="BORING", category="MACHINING", description="Internal diameter operations"),
        Capability(name="THREADING", category="MACHINING", description="Thread cutting operations"),
        Capability(name="GRINDING", category="FINISHING", description="Precision surface finishing"),
        Capability(name="CMM_INSPECTION", category="INSPECTION", description="Coordinate measuring"),
        Capability(name="OPTICAL_INSPECTION", category="INSPECTION", description="Non-contact measurement"),
        Capability(name="SURFACE_PROFILING", category="INSPECTION", description="Surface finish measurement"),
    ]

    session.bulk_save_objects(capabilities)
    session.commit()
    session.close()
    print("✓ Seeded capabilities")


def seed_materials():
    """Seed material specifications"""
    session = SessionLocal()

    materials = [
        Material(
            name="Aluminum 6061-T6",
            material_type="METAL",
            grade="6061-T6",
            hardness=95,
            tensile_strength=310,
            density=2.7,
            machinability_rating=90,
            cost_per_kg=8.50
        ),
        Material(
            name="Steel 1018",
            material_type="METAL",
            grade="1018",
            hardness=126,
            tensile_strength=440,
            density=7.87,
            machinability_rating=70,
            cost_per_kg=2.50
        ),
        Material(
            name="Stainless Steel 316",
            material_type="METAL",
            grade="316",
            hardness=217,
            tensile_strength=579,
            density=8.0,
            machinability_rating=45,
            cost_per_kg=12.00
        ),
        Material(
            name="Titanium Ti-6Al-4V",
            material_type="METAL",
            grade="Ti-6Al-4V",
            hardness=334,
            tensile_strength=950,
            density=4.43,
            machinability_rating=30,
            cost_per_kg=45.00
        ),
        Material(
            name="Brass C360",
            material_type="METAL",
            grade="C360",
            hardness=100,
            tensile_strength=469,
            density=8.5,
            machinability_rating=100,
            cost_per_kg=11.00
        ),
    ]

    session.bulk_save_objects(materials)
    session.commit()
    session.close()
    print("✓ Seeded materials")


def seed_machines():
    """Seed machine catalog"""
    session = SessionLocal()

    # Get capabilities and materials for relationships
    turning_cap = session.query(Capability).filter_by(name="TURNING").first()
    milling_cap = session.query(Capability).filter_by(name="MILLING").first()
    drilling_cap = session.query(Capability).filter_by(name="DRILLING").first()
    cmm_cap = session.query(Capability).filter_by(name="CMM_INSPECTION").first()

    aluminum = session.query(Material).filter_by(name="Aluminum 6061-T6").first()
    steel = session.query(Material).filter_by(name="Steel 1018").first()
    stainless = session.query(Material).filter_by(name="Stainless Steel 316").first()
    titanium = session.query(Material).filter_by(name="Titanium Ti-6Al-4V").first()
    brass = session.query(Material).filter_by(name="Brass C360").first()

    machines = [
        Machine(
            name="Haas ST-30",
            manufacturer="Haas Automation",
            model="ST-30",
            category="CNC_LATHE",
            price=185000,
            max_part_size_x=762,
            max_part_size_y=305,
            max_part_size_z=305,
            spindle_speed_max=3000,
            feed_rate_max=1000,
            tolerance=0.005,
            repeatability=0.0025,
            cycle_time_factor=1.0,
            maintenance_interval=2000,
            power_consumption=30,
            floor_space=15,
            features=json.dumps({
                "live_tooling": True,
                "sub_spindle": False,
                "bar_feeder": True,
                "chip_conveyor": True
            }),
            automation_level="SEMI_AUTO",
            control_system="HAAS",
            is_available=True,
            lead_time_weeks=12,
            description="High-performance CNC lathe for precision turning operations",
            capabilities=[turning_cap, drilling_cap],
            compatible_materials=[aluminum, steel, stainless, brass]
        ),
        Machine(
            name="Haas VF-3",
            manufacturer="Haas Automation",
            model="VF-3",
            category="CNC_MILL",
            price=145000,
            max_part_size_x=1016,
            max_part_size_y=508,
            max_part_size_z=635,
            spindle_speed_max=8100,
            feed_rate_max=12700,
            tolerance=0.008,
            repeatability=0.005,
            cycle_time_factor=1.0,
            maintenance_interval=2500,
            power_consumption=25,
            floor_space=12,
            features=json.dumps({
                "tool_changer_capacity": 24,
                "coolant_through_spindle": True,
                "probing_system": True
            }),
            automation_level="SEMI_AUTO",
            control_system="HAAS",
            is_available=True,
            lead_time_weeks=10,
            description="3-axis vertical machining center for milling operations",
            capabilities=[milling_cap, drilling_cap],
            compatible_materials=[aluminum, steel, stainless, titanium, brass]
        ),
        Machine(
            name="DMG MORI NLX 2500",
            manufacturer="DMG MORI",
            model="NLX 2500",
            category="CNC_LATHE",
            price=285000,
            max_part_size_x=650,
            max_part_size_y=350,
            max_part_size_z=350,
            spindle_speed_max=4000,
            feed_rate_max=1500,
            tolerance=0.003,
            repeatability=0.001,
            cycle_time_factor=0.85,
            maintenance_interval=3000,
            power_consumption=35,
            floor_space=18,
            features=json.dumps({
                "live_tooling": True,
                "sub_spindle": True,
                "y_axis": True,
                "automatic_tool_measurement": True
            }),
            automation_level="FULLY_AUTO",
            control_system="SIEMENS",
            is_available=True,
            lead_time_weeks=16,
            description="Advanced CNC lathe with Y-axis and sub-spindle",
            capabilities=[turning_cap, milling_cap, drilling_cap],
            compatible_materials=[aluminum, steel, stainless, titanium, brass]
        ),
        Machine(
            name="Mazak Variaxis i-600",
            manufacturer="Mazak",
            model="Variaxis i-600",
            category="5_AXIS_MILL",
            price=495000,
            max_part_size_x=600,
            max_part_size_y=600,
            max_part_size_z=500,
            spindle_speed_max=12000,
            feed_rate_max=20000,
            tolerance=0.005,
            repeatability=0.002,
            cycle_time_factor=0.7,
            maintenance_interval=3500,
            power_consumption=45,
            floor_space=25,
            features=json.dumps({
                "5_axis_simultaneous": True,
                "tool_changer_capacity": 60,
                "automatic_pallet_changer": True,
                "in_process_measurement": True
            }),
            automation_level="FULLY_AUTO",
            control_system="MAZATROL",
            is_available=True,
            lead_time_weeks=20,
            description="5-axis vertical machining center for complex parts",
            capabilities=[milling_cap, drilling_cap],
            compatible_materials=[aluminum, steel, stainless, titanium, brass]
        ),
    ]

    session.bulk_save_objects(machines)
    session.commit()
    print("✓ Seeded machines")

    # Add quality tools
    zeiss_cmm = QualityTool(
        name="Zeiss Contura G2",
        manufacturer="Carl Zeiss",
        tool_type="CMM",
        measurement_range_min=0.001,
        measurement_range_max=700,
        accuracy=0.0015,
        resolution=0.0001,
        price=125000,
        calibration_interval_days=365,
        is_automated=True,
        has_spc_capability=True,
        software_included="Calypso",
        description="High-precision coordinate measuring machine",
    )

    mitutoyo_cmm = QualityTool(
        name="Mitutoyo Crysta-Apex S",
        manufacturer="Mitutoyo",
        tool_type="CMM",
        measurement_range_min=0.001,
        measurement_range_max=900,
        accuracy=0.0018,
        resolution=0.0001,
        price=95000,
        calibration_interval_days=365,
        is_automated=True,
        has_spc_capability=True,
        software_included="MCOSMOS",
        description="CNC coordinate measuring machine",
    )

    keyence_optical = QualityTool(
        name="Keyence IM-8000",
        manufacturer="Keyence",
        tool_type="OPTICAL_CMM",
        measurement_range_min=0.0001,
        measurement_range_max=200,
        accuracy=0.003,
        resolution=0.0001,
        price=75000,
        calibration_interval_days=180,
        is_automated=True,
        has_spc_capability=True,
        software_included="IM Series Software",
        description="High-speed optical measuring system",
    )

    session.add_all([zeiss_cmm, mitutoyo_cmm, keyence_optical])
    session.commit()
    session.close()
    print("✓ Seeded quality tools")


def seed_quality_standards():
    """Seed quality standards database"""
    session = SessionLocal()

    standards = [
        QualityStandard(
            standard_id="ISO-9001:2015",
            title="Quality management systems — Requirements",
            organization="ISO",
            category="QUALITY_MANAGEMENT",
            full_text="""ISO 9001:2015 specifies requirements for a quality management system when an organization:
            a) needs to demonstrate its ability to consistently provide products and services that meet customer and applicable statutory and regulatory requirements
            b) aims to enhance customer satisfaction through the effective application of the system

            Key requirements include:
            - Context of the organization (understanding needs and expectations)
            - Leadership and commitment
            - Risk-based thinking
            - Process approach
            - Customer focus
            - Continual improvement

            The standard promotes the adoption of a process approach when developing, implementing and improving the effectiveness of a quality management system.""",
            summary="ISO 9001:2015 sets out criteria for quality management systems focusing on customer satisfaction and continual improvement",
            key_requirements=json.dumps([
                "Document control procedures",
                "Management review process",
                "Internal audit program",
                "Corrective action procedures",
                "Preventive action procedures",
                "Control of nonconforming product"
            ]),
            industry=json.dumps(["manufacturing", "aerospace", "automotive", "medical", "electronics"]),
            applicable_processes=json.dumps(["all"]),
            version="2015",
            publication_date=datetime(2015, 9, 15)
        ),
        QualityStandard(
            standard_id="AS9100D",
            title="Quality Management Systems - Requirements for Aviation, Space and Defense Organizations",
            organization="SAE",
            category="QUALITY_MANAGEMENT",
            full_text="""AS9100D is a widely adopted and standardized quality management system for the aerospace industry.

            It includes all ISO 9001:2015 requirements plus additional aerospace-specific requirements such as:
            - Configuration management
            - Product safety
            - Risk management
            - First article inspection
            - Advanced product quality planning
            - On-time delivery performance

            Special processes requirements:
            - All special processes must be controlled and validated
            - Personnel performing special processes must be qualified
            - Records of qualification and requalification must be maintained

            The standard emphasizes prevention of defects and reduction of variation and waste in the supply chain.""",
            summary="AS9100D extends ISO 9001 for aerospace manufacturing with emphasis on safety and reliability",
            key_requirements=json.dumps([
                "Configuration management",
                "First article inspection (FAI)",
                "Counterfeit parts prevention",
                "Foreign object debris (FOD) prevention",
                "Critical items control",
                "Key characteristics identification"
            ]),
            industry=json.dumps(["aerospace", "defense", "space"]),
            applicable_processes=json.dumps(["machining", "assembly", "testing", "inspection"]),
            version="D",
            publication_date=datetime(2016, 9, 1)
        ),
        QualityStandard(
            standard_id="ASME-Y14.5-2018",
            title="Dimensioning and Tolerancing",
            organization="ASME",
            category="DIMENSIONAL",
            full_text="""ASME Y14.5-2018 establishes uniform practices for stating and interpreting dimensioning, tolerancing, and related requirements.

            Key concepts include:

            Geometric Dimensioning and Tolerancing (GD&T):
            - Form tolerances (straightness, flatness, circularity, cylindricity)
            - Orientation tolerances (perpendicularity, angularity, parallelism)
            - Location tolerances (position, concentricity, symmetry)
            - Profile tolerances (profile of a line, profile of a surface)
            - Runout tolerances (circular runout, total runout)

            Datum reference frames:
            - Primary, secondary, and tertiary datums
            - Datum feature simulators
            - Maximum material condition (MMC)
            - Least material condition (LMC)
            - Regardless of feature size (RFS)

            The standard provides precise language for communicating design intent and inspection requirements.""",
            summary="ASME Y14.5-2018 defines the language of GD&T for precise dimensional control",
            key_requirements=json.dumps([
                "Datum reference frame establishment",
                "Feature control frame usage",
                "Material condition modifiers",
                "Tolerance stack-up analysis",
                "Inspection planning based on GD&T"
            ]),
            industry=json.dumps(["manufacturing", "aerospace", "automotive", "medical"]),
            applicable_processes=json.dumps(["design", "machining", "inspection", "quality_control"]),
            version="2018",
            publication_date=datetime(2018, 2, 22)
        ),
        QualityStandard(
            standard_id="ISO-1101:2017",
            title="Geometrical product specifications (GPS) — Geometrical tolerancing — Tolerances of form, orientation, location and run-out",
            organization="ISO",
            category="DIMENSIONAL",
            full_text="""ISO 1101:2017 defines geometrical tolerancing to control form, orientation, location and run-out.

            Tolerance types covered:

            Form tolerances:
            - Straightness: Controls how much a line element can deviate from perfect straightness
            - Flatness: Controls the variation of a surface from a perfect plane
            - Roundness (Circularity): Controls deviation from a perfect circle
            - Cylindricity: Controls the form of a cylindrical surface

            Orientation tolerances:
            - Parallelism: Controls how parallel a feature is to a datum
            - Perpendicularity: Controls how perpendicular a feature is to a datum
            - Angularity: Controls the angle of a feature relative to a datum

            Location tolerances:
            - Position: Controls the location of a feature relative to datums
            - Concentricity: Controls the common center of features
            - Symmetry: Controls the median points of features

            The standard is compatible with but distinct from ASME Y14.5.""",
            summary="ISO 1101:2017 provides international standards for geometric tolerancing",
            key_requirements=json.dumps([
                "Tolerance zone definition",
                "Datum system specification",
                "Material condition application",
                "Verification principles"
            ]),
            industry=json.dumps(["manufacturing", "automotive", "medical", "aerospace"]),
            applicable_processes=json.dumps(["design", "machining", "inspection"]),
            version="2017",
            publication_date=datetime(2017, 2, 1)
        ),
        QualityStandard(
            standard_id="IATF-16949:2016",
            title="Quality management system requirements for automotive production",
            organization="IATF",
            category="QUALITY_MANAGEMENT",
            full_text="""IATF 16949:2016 defines quality management system requirements for automotive production and relevant service parts.

            Key automotive-specific requirements:

            Advanced Product Quality Planning (APQP):
            - Product design and development process
            - Process design and development
            - Product and process validation
            - Feedback, assessment, and corrective action

            Production Part Approval Process (PPAP):
            - Design records
            - Engineering change documentation
            - Process flow diagrams
            - Process FMEA
            - Control plans
            - Measurement system analysis (MSA)
            - Dimensional results
            - Material and performance test results

            Manufacturing process requirements:
            - Error-proofing (poka-yoke)
            - Preventive and predictive maintenance
            - Total productive maintenance (TPM)
            - Management of production tooling

            The standard emphasizes defect prevention and variation reduction in the supply chain.""",
            summary="IATF 16949:2016 extends ISO 9001 for automotive manufacturing with APQP and PPAP requirements",
            key_requirements=json.dumps([
                "APQP implementation",
                "PPAP submission",
                "Control plan development",
                "FMEA (Failure Mode Effects Analysis)",
                "MSA (Measurement System Analysis)",
                "Statistical Process Control (SPC)"
            ]),
            industry=json.dumps(["automotive"]),
            applicable_processes=json.dumps(["machining", "assembly", "testing", "inspection", "heat_treatment"]),
            version="2016",
            publication_date=datetime(2016, 10, 1)
        ),
        QualityStandard(
            standard_id="ISO-13485:2016",
            title="Medical devices — Quality management systems — Requirements for regulatory purposes",
            organization="ISO",
            category="QUALITY_MANAGEMENT",
            full_text="""ISO 13485:2016 specifies requirements for a quality management system for medical device manufacturing.

            Key medical device-specific requirements:

            Risk management:
            - Risk analysis throughout product lifecycle
            - Integration with ISO 14971 (Risk management for medical devices)
            - Risk-based approach to design and manufacturing

            Design and development:
            - Design and development planning
            - Design inputs and outputs
            - Design review, verification, and validation
            - Design transfer
            - Design changes

            Sterile medical devices:
            - Cleanliness of product
            - Sterile barrier systems
            - Sterilization process validation

            Implantable devices:
            - Traceability requirements
            - Record retention

            The standard requires strict documentation, validation, and traceability to ensure patient safety.""",
            summary="ISO 13485:2016 provides quality system requirements for medical device manufacturers",
            key_requirements=json.dumps([
                "Risk management integration",
                "Design control procedures",
                "Process validation",
                "Sterilization validation (if applicable)",
                "Full traceability",
                "Medical device reporting (MDR)",
                "Post-market surveillance"
            ]),
            industry=json.dumps(["medical", "pharmaceutical"]),
            applicable_processes=json.dumps(["machining", "assembly", "inspection", "sterilization", "packaging"]),
            version="2016",
            publication_date=datetime(2016, 3, 1)
        ),
    ]

    session.bulk_save_objects(standards)
    session.commit()
    session.close()
    print("✓ Seeded quality standards")


def seed_quality_plan_templates():
    """Seed quality plan templates"""
    session = SessionLocal()

    templates = [
        QualityPlanTemplate(
            name="Precision Machined Part - Aerospace",
            description="Quality plan for precision machined aerospace components",
            part_types=json.dumps(["rotational", "prismatic"]),
            industries=json.dumps(["aerospace", "defense"]),
            complexity_level="HIGH",
            inspection_points=json.dumps([
                {
                    "feature": "Critical dimensions",
                    "method": "CMM",
                    "frequency": "First piece and every 10 parts",
                    "sample_size": 3
                },
                {
                    "feature": "Surface finish",
                    "method": "Profilometer",
                    "frequency": "First and last piece per shift",
                    "sample_size": 3
                },
                {
                    "feature": "Concentricity",
                    "method": "CMM",
                    "frequency": "Every part",
                    "sample_size": 1
                }
            ]),
            control_methods=json.dumps([
                "Statistical Process Control (SPC)",
                "First Article Inspection (FAI)",
                "In-process inspection",
                "Final inspection"
            ]),
            acceptance_criteria=json.dumps({
                "dimensional": "All dimensions within drawing tolerances",
                "surface_finish": "Ra ≤ specified value",
                "visual": "No visible defects",
                "cpk": "Cpk ≥ 1.67"
            }),
            documentation_requirements=json.dumps([
                "FAI report (AS9102)",
                "Control plan",
                "Process FMEA",
                "Inspection records",
                "SPC charts",
                "Certificate of Conformance"
            ]),
            related_standards=json.dumps(["AS9100D", "ASME-Y14.5-2018", "ISO-1101:2017"])
        ),
        QualityPlanTemplate(
            name="Automotive Production Part",
            description="Quality plan for automotive production components",
            part_types=json.dumps(["rotational", "prismatic", "stamped"]),
            industries=json.dumps(["automotive"]),
            complexity_level="MEDIUM",
            inspection_points=json.dumps([
                {
                    "feature": "Key characteristics",
                    "method": "CMM or gauging",
                    "frequency": "Per control plan (typically every 2 hours)",
                    "sample_size": 5
                },
                {
                    "feature": "Appearance",
                    "method": "Visual inspection",
                    "frequency": "Every part",
                    "sample_size": 1
                }
            ]),
            control_methods=json.dumps([
                "Statistical Process Control (SPC) on key characteristics",
                "100% visual inspection",
                "Periodic dimensional inspection",
                "Error-proofing (poka-yoke)"
            ]),
            acceptance_criteria=json.dumps({
                "dimensional": "Within specification limits",
                "cpk": "Cpk ≥ 1.33",
                "appearance": "Per appearance approval report (AAR)",
                "defect_rate": "< 50 PPM"
            }),
            documentation_requirements=json.dumps([
                "PPAP package",
                "Control plan",
                "Process FMEA",
                "MSA studies",
                "Run at rate study",
                "Appearance approval report (AAR)"
            ]),
            related_standards=json.dumps(["IATF-16949:2016", "ASME-Y14.5-2018"])
        ),
        QualityPlanTemplate(
            name="Medical Device Component",
            description="Quality plan for medical device manufacturing",
            part_types=json.dumps(["rotational", "prismatic"]),
            industries=json.dumps(["medical"]),
            complexity_level="CRITICAL",
            inspection_points=json.dumps([
                {
                    "feature": "Critical dimensions",
                    "method": "CMM with calibrated tooling",
                    "frequency": "100% inspection or validated sampling plan",
                    "sample_size": "Per sampling plan"
                },
                {
                    "feature": "Surface finish",
                    "method": "Profilometer",
                    "frequency": "First, middle, last piece per batch",
                    "sample_size": 3
                },
                {
                    "feature": "Cleanliness",
                    "method": "Visual inspection in clean room",
                    "frequency": "100%",
                    "sample_size": 1
                },
                {
                    "feature": "Material verification",
                    "method": "Material certification + testing",
                    "frequency": "Per lot",
                    "sample_size": "Per lot"
                }
            ]),
            control_methods=json.dumps([
                "Validated manufacturing process",
                "100% traceability",
                "Statistical Process Control",
                "Environmental controls",
                "Material traceability"
            ]),
            acceptance_criteria=json.dumps({
                "dimensional": "All dimensions within specification",
                "cpk": "Cpk ≥ 2.0 for critical characteristics",
                "traceability": "Full traceability to raw material",
                "cleanliness": "Meets cleanliness specification",
                "biocompatibility": "Meets biocompatibility requirements (if applicable)"
            }),
            documentation_requirements=json.dumps([
                "Device Master Record (DMR)",
                "Device History Record (DHR)",
                "Process validation protocol and report",
                "Inspection and test records",
                "Certificate of Conformance",
                "Material certifications",
                "Traceability records"
            ]),
            related_standards=json.dumps(["ISO-13485:2016", "ASME-Y14.5-2018", "ISO-14971"])
        ),
    ]

    session.bulk_save_objects(templates)
    session.commit()
    session.close()
    print("✓ Seeded quality plan templates")


def main():
    """Run all seed functions"""
    print("\n🌱 Seeding Manufacturing Database...")
    print("=" * 50)

    seed_capabilities()
    seed_materials()
    seed_machines()
    seed_quality_standards()
    seed_quality_plan_templates()

    print("=" * 50)
    print("✅ Database seeding completed successfully!\n")


if __name__ == "__main__":
    main()
