# Jaque.ai Manufacturing Operations Platform

A production-ready manufacturing operations platform that provides AI-powered quality control, CAD analysis, production monitoring, and analytics capabilities.

## Features

### 🎯 Core Capabilities

- **CAD File Upload & Analysis**: Support for multiple CAD formats (.dwg, .step, .iges, .stl, .3dm, .x_t)
- **Quality Control Planning**: AI-generated quality strategies and inspection plans
- **Manufacturing Setup**: Equipment recommendations and process flow optimization
- **Production Monitoring**: Real-time PLC integration and OEE tracking
- **Quality Analytics**: Statistical Process Control (SPC) charts and AI-powered insights

### ✨ Key Features

- Clean, minimalist UI design
- Fully accessible (WCAG 2.1 compliant)
- Responsive design for all devices
- Real-time data visualization
- Drag-and-drop file upload
- Interactive workflow navigation
- Production-ready error handling

## Project Structure

```
manufacturing/
├── index.html              # Main HTML file
├── assets/
│   ├── css/
│   │   └── styles.css      # Production stylesheet
│   └── js/
│       └── app.js          # Main application JavaScript
├── docs/                   # Additional documentation
├── package.json            # Project metadata
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.x (for local development server) or any other HTTP server

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YouhannaM/Jaque-landing-page.git
cd Jaque-landing-page/manufacturing
```

2. Start a local development server:

**Using Python 3:**
```bash
python3 -m http.server 8000
```

**Or using Python 2:**
```bash
python -m SimpleHTTPServer 8000
```

**Or using Node.js (if you have it installed):**
```bash
npx http-server -p 8000
```

3. Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

### Workflow Steps

#### Step 1: CAD Upload
1. Drag and drop CAD files or click to select files
2. Enter part name and specifications
3. Select material type
4. Specify annual production volume
5. Click "Analyze & Generate Proposal"

#### Step 2: Quality Plan
- Review AI-generated quality control plan
- Examine critical dimensions and measurement methods
- Review control plan and quality strategy
- Approve plan or request changes

#### Step 3: Tooling & Process
- Review equipment recommendations
- Analyze process flow and cycle times
- Review cost estimates
- Approve process or request changes

#### Step 4: Production Monitoring
- View real-time production metrics (OEE, parts count, etc.)
- Monitor predictive maintenance alerts
- Log quality data for parts
- Track process capability

#### Step 5: Quality Analytics
- View SPC charts for critical dimensions
- Analyze process capability metrics
- Review AI-powered insights and recommendations
- Track corrective actions

## Technical Details

### Technologies Used

- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern responsive design with Flexbox and Grid
- **Vanilla JavaScript**: No framework dependencies, ES6+ features
- **Canvas API**: For chart rendering

### Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Accessibility Features

- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Skip to main content link
- Semantic HTML structure
- High contrast design
- Focus indicators

### Performance Optimizations

- Minimal external dependencies
- Efficient DOM manipulation
- Debounced event handlers
- Lazy chart rendering
- Optimized asset loading

## Configuration

### Customization

You can customize the platform by modifying:

**Colors and Branding** (`assets/css/styles.css`):
```css
/* Update these variables for your brand */
:root {
    --primary-color: #000000;
    --secondary-color: #666666;
    --background-color: #ffffff;
}
```

**Application Settings** (`assets/js/app.js`):
```javascript
// Modify intervals and settings in the ManufacturingApp class
this.productionMonitoringInterval = 5000; // 5 seconds
this.metricsUpdateInterval = 10000; // 10 seconds
```

## Development

### Code Structure

The application follows object-oriented principles with a single `ManufacturingApp` class that handles:

- Event listeners and user interactions
- File upload and validation
- Workflow navigation
- Data management
- Chart rendering
- Production monitoring

### Error Handling

The application includes comprehensive error handling:
- File validation
- Form validation
- XSS prevention (HTML escaping)
- Graceful degradation
- User-friendly error messages

### Security Considerations

- Content Security Policy headers
- HTML escaping to prevent XSS
- Input validation
- No external dependencies (reduced attack surface)

## Deployment

### Static Hosting

The platform can be deployed to any static hosting service:

**GitHub Pages:**
```bash
# Already configured in the repository
```

**Netlify:**
```bash
# Deploy the manufacturing directory
netlify deploy --dir=manufacturing --prod
```

**Vercel:**
```bash
# Deploy the manufacturing directory
vercel --prod
```

**AWS S3:**
```bash
aws s3 sync manufacturing/ s3://your-bucket-name/ --acl public-read
```

### Docker Deployment

You can use the project's existing Docker setup:

```bash
# From the root directory
docker-compose up
```

## API Integration

The platform is designed to integrate with backend APIs. To connect to your manufacturing backend:

1. Update API endpoints in `assets/js/app.js`
2. Implement authentication (JWT, OAuth, etc.)
3. Add API calls in relevant methods (analyzeCAD, logQualityData, etc.)

Example:
```javascript
async analyzeCAD() {
    const response = await fetch('/api/analyze-cad', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            partName: this.partName,
            material: this.material,
            volume: this.volume
        })
    });
    const data = await response.json();
    // Handle response
}
```

## Testing

Currently, the platform includes manual testing procedures. To add automated tests:

1. Install a testing framework (Jest, Mocha, etc.)
2. Create test files in a `tests/` directory
3. Add test scripts to `package.json`

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Contact: support@jaque.ai

## Roadmap

- [ ] Backend API integration
- [ ] Real-time WebSocket support for live updates
- [ ] Advanced charting library integration (Chart.js, D3.js)
- [ ] PDF report generation
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Integration with ERP systems

## Acknowledgments

Built with modern web standards and best practices for manufacturing operations.

---

**Version**: 1.0.0
**Last Updated**: November 2025
**Maintained by**: Jaque.ai Team
