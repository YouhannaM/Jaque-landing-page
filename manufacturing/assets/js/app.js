/**
 * ManufactureFlow - Manufacturing Operations Platform
 * Main Application JavaScript
 * Version: 1.0.0
 */

(function() {
    'use strict';

    /**
     * Main Application Class
     */
    class ManufacturingApp {
        constructor() {
            this.currentStep = 1;
            this.uploadedFiles = [];
            this.qualityData = [];
            this.productionMonitoringInterval = null;
            this.metricsUpdateInterval = null;

            this.init();
        }

        /**
         * Initialize the application
         */
        init() {
            this.setupEventListeners();
            this.initializeData();
            console.log('ManufacturingApp initialized');
        }

        /**
         * Setup all event listeners
         */
        setupEventListeners() {
            // Navigation
            document.querySelectorAll('.nav-step').forEach(step => {
                step.addEventListener('click', (e) => this.handleNavClick(e));
                step.addEventListener('keydown', (e) => this.handleNavKeydown(e));
            });

            // File upload
            this.setupFileUpload();

            // Forms
            this.setupForms();
        }

        /**
         * Handle navigation click
         */
        handleNavClick(e) {
            const stepNum = parseInt(e.currentTarget.dataset.step);
            if (stepNum <= this.currentStep) {
                this.showStep(stepNum);
            }
        }

        /**
         * Handle navigation keyboard events
         */
        handleNavKeydown(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.handleNavClick(e);
            }
        }

        /**
         * Setup file upload functionality
         */
        setupFileUpload() {
            const uploadArea = document.getElementById('uploadArea');
            if (!uploadArea) return;

            // Drag and drop events
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = Array.from(e.dataTransfer.files);
                this.handleFiles(files);
            });

            // Click to upload
            uploadArea.addEventListener('click', () => {
                this.openFileDialog();
            });

            // Keyboard support
            uploadArea.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.openFileDialog();
                }
            });
        }

        /**
         * Setup form event listeners
         */
        setupForms() {
            const cadForm = document.getElementById('cadForm');
            if (cadForm) {
                cadForm.addEventListener('submit', (e) => {
                    e.preventDefault();
                    this.analyzeCAD();
                });
            }

            const qualityForm = document.getElementById('qualityDataForm');
            if (qualityForm) {
                qualityForm.addEventListener('submit', (e) => {
                    e.preventDefault();
                    this.logQualityData();
                });
            }
        }

        /**
         * Open file dialog
         */
        openFileDialog() {
            const input = document.createElement('input');
            input.type = 'file';
            input.multiple = true;
            input.accept = '.dwg,.step,.iges,.stl,.3dm,.x_t';
            input.onchange = (e) => this.handleFiles(Array.from(e.target.files));
            input.click();
        }

        /**
         * Handle uploaded files
         */
        handleFiles(files) {
            if (!files || files.length === 0) {
                console.warn('No files selected');
                return;
            }

            // Validate files
            const validFiles = files.filter(file => {
                const extension = file.name.split('.').pop().toLowerCase();
                const validExtensions = ['dwg', 'step', 'iges', 'stl', '3dm', 'x_t'];
                return validExtensions.includes(extension);
            });

            if (validFiles.length === 0) {
                this.showError('Please upload valid CAD files');
                return;
            }

            this.uploadedFiles = validFiles;
            this.displayUploadedFiles();
        }

        /**
         * Display uploaded files
         */
        displayUploadedFiles() {
            const fileList = document.getElementById('fileList');
            const filesContainer = document.getElementById('files');

            if (!fileList || !filesContainer) return;

            fileList.classList.remove('hidden');
            filesContainer.innerHTML = '';

            this.uploadedFiles.forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.setAttribute('role', 'listitem');
                fileItem.innerHTML = `
                    <span>${this.escapeHtml(file.name)}</span>
                    <span>${(file.size / 1024 / 1024).toFixed(2)} MB</span>
                `;
                filesContainer.appendChild(fileItem);
            });
        }

        /**
         * Analyze CAD files
         */
        analyzeCAD() {
            if (this.uploadedFiles.length === 0) {
                this.showError('Please upload CAD files');
                return;
            }

            const partName = document.getElementById('partName')?.value;
            const materialType = document.getElementById('materialType')?.value;
            const volume = document.getElementById('volume')?.value;

            if (!partName || !materialType || !volume) {
                this.showError('Please complete all required fields');
                return;
            }

            this.showLoading(true);

            // Create progress indicator
            const progressBar = document.createElement('div');
            progressBar.className = 'progress-bar';
            progressBar.innerHTML = '<div class="progress-fill" style="width: 0%"></div>';

            const analysisDiv = document.createElement('div');
            analysisDiv.innerHTML = '<h3>Analyzing CAD Files...</h3>';
            analysisDiv.appendChild(progressBar);

            const step1 = document.getElementById('step1');
            step1?.appendChild(analysisDiv);

            // Simulate analysis with progress
            let progress = 0;
            const interval = setInterval(() => {
                progress += 10;
                const fillElement = progressBar.querySelector('.progress-fill');
                if (fillElement) {
                    fillElement.style.width = progress + '%';
                }

                if (progress >= 100) {
                    clearInterval(interval);
                    setTimeout(() => {
                        this.currentStep = 2;
                        this.showStep(2);
                        analysisDiv.remove();
                        this.showLoading(false);
                    }, 500);
                }
            }, 200);
        }

        /**
         * Approve quality plan and move to next step
         */
        approveQualityPlan() {
            this.currentStep = 3;
            this.showStep(3);
        }

        /**
         * Request revisions
         */
        requestRevisions() {
            this.showNotification('Revision request submitted. Engineers will contact you within 24 hours.', 'info');
        }

        /**
         * Approve process and start production
         */
        approveProcess() {
            this.currentStep = 4;
            this.showStep(4);
            this.startProductionMonitoring();
        }

        /**
         * Request process revisions
         */
        requestProcessRevisions() {
            this.showNotification('Process revision request submitted for review.', 'info');
        }

        /**
         * Start production monitoring
         */
        startProductionMonitoring() {
            // Clear any existing interval
            if (this.productionMonitoringInterval) {
                clearInterval(this.productionMonitoringInterval);
            }

            this.productionMonitoringInterval = setInterval(() => {
                this.updateProductionMetrics();
            }, 5000);
        }

        /**
         * Update production metrics
         */
        updateProductionMetrics() {
            const oeeElement = document.getElementById('oeeValue');
            if (oeeElement) {
                const currentOEE = parseInt(oeeElement.textContent);
                const newOEE = Math.max(75, Math.min(95, currentOEE + (Math.random() - 0.5) * 4));
                oeeElement.textContent = Math.round(newOEE) + '%';
            }
        }

        /**
         * Log quality data
         */
        logQualityData() {
            const operator = document.getElementById('operator')?.value;
            const serialNumber = document.getElementById('serialNumber')?.value;
            const boreDiameter = document.getElementById('boreDiameter')?.value;
            const overallLength = document.getElementById('overallLength')?.value;

            if (!operator || !serialNumber || !boreDiameter || !overallLength) {
                this.showError('Please complete all fields');
                return;
            }

            const dataPoint = {
                timestamp: new Date(),
                operator,
                serialNumber,
                boreDiameter: parseFloat(boreDiameter),
                overallLength: parseFloat(overallLength)
            };

            this.qualityData.push(dataPoint);

            // Clear form
            const form = document.getElementById('qualityDataForm');
            if (form) {
                document.getElementById('serialNumber').value = '';
                document.getElementById('boreDiameter').value = '';
                document.getElementById('overallLength').value = '';
            }

            // Show success message
            const successDiv = document.createElement('div');
            successDiv.className = 'alert alert-success';
            successDiv.setAttribute('role', 'status');
            successDiv.innerHTML = `<strong>Data Logged:</strong> Part ${this.escapeHtml(serialNumber)} recorded successfully.`;

            const step4 = document.getElementById('step4');
            step4?.appendChild(successDiv);

            setTimeout(() => successDiv.remove(), 3000);

            // Enable analytics step
            this.currentStep = Math.max(this.currentStep, 5);
        }

        /**
         * Show specific step
         */
        showStep(step) {
            // Hide all steps
            document.querySelectorAll('.step-content').forEach(content => {
                content.classList.remove('active');
            });

            // Show selected step
            const stepElement = document.getElementById(`step${step}`);
            if (stepElement) {
                stepElement.classList.add('active');
            }

            // Update navigation
            document.querySelectorAll('.nav-step').forEach(nav => {
                nav.classList.remove('active');
                nav.removeAttribute('aria-current');

                const navStep = parseInt(nav.dataset.step);
                if (navStep < step) {
                    nav.classList.add('completed');
                } else {
                    nav.classList.remove('completed');
                }
            });

            const activeNav = document.querySelector(`[data-step="${step}"]`);
            if (activeNav) {
                activeNav.classList.add('active');
                activeNav.setAttribute('aria-current', 'step');
            }

            // Initialize charts if on analytics step
            if (step === 5) {
                setTimeout(() => this.initializeCharts(), 100);
            }

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        /**
         * Initialize charts
         */
        initializeCharts() {
            this.drawSPCChart();
            this.drawCapabilityChart();
        }

        /**
         * Draw SPC Chart
         */
        drawSPCChart() {
            const canvas = document.getElementById('spcChart');
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            if (!ctx) return;

            const measurements = [];
            const ucl = 25.005;
            const lcl = 24.995;
            const target = 25.000;

            // Generate sample measurements
            for (let i = 0; i < 30; i++) {
                measurements.push(target + (Math.random() - 0.5) * 0.008);
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Control limits
            ctx.strokeStyle = '#666666';
            ctx.setLineDash([2, 2]);
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(50, 50);
            ctx.lineTo(350, 50);
            ctx.moveTo(50, 250);
            ctx.lineTo(350, 250);
            ctx.stroke();

            // Target line
            ctx.strokeStyle = '#000000';
            ctx.setLineDash([]);
            ctx.beginPath();
            ctx.moveTo(50, 150);
            ctx.lineTo(350, 150);
            ctx.stroke();

            // Data points
            ctx.strokeStyle = '#000000';
            ctx.fillStyle = '#000000';
            ctx.lineWidth = 1;
            ctx.beginPath();

            for (let i = 0; i < measurements.length; i++) {
                const x = 50 + (i * 300 / measurements.length);
                const y = 250 - ((measurements[i] - 24.995) / 0.01) * 200;

                if (i === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }

                ctx.fillRect(x - 1, y - 1, 2, 2);
            }
            ctx.stroke();

            // Labels
            ctx.fillStyle = '#666666';
            ctx.font = '11px Helvetica Neue';
            ctx.fillText('25.005', 355, 54);
            ctx.fillText('25.000', 355, 154);
            ctx.fillText('24.995', 355, 254);
        }

        /**
         * Draw Capability Chart
         */
        drawCapabilityChart() {
            const canvas = document.getElementById('capabilityChart');
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            if (!ctx) return;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const bars = [5, 12, 25, 35, 28, 15, 8, 3];
            const maxBar = Math.max(...bars);

            ctx.fillStyle = '#000000';
            for (let i = 0; i < bars.length; i++) {
                const x = 50 + i * 35;
                const height = (bars[i] / maxBar) * 200;
                const y = 250 - height;

                ctx.fillRect(x, y, 25, height);
            }

            // Labels
            ctx.fillStyle = '#666666';
            ctx.font = '12px Helvetica Neue';
            ctx.fillText('Cp: 1.52', 50, 30);
            ctx.fillText('Cpk: 1.45', 130, 30);
            ctx.fillText('Pp: 1.48', 210, 30);
            ctx.fillText('Ppk: 1.41', 290, 30);
        }

        /**
         * Initialize sample data
         */
        initializeData() {
            this.qualityData = [
                {
                    timestamp: new Date(Date.now() - 3600000),
                    operator: 'John Smith',
                    serialNumber: 'P001',
                    boreDiameter: 25.002,
                    overallLength: 149.98
                },
                {
                    timestamp: new Date(Date.now() - 7200000),
                    operator: 'Maria Garcia',
                    serialNumber: 'P002',
                    boreDiameter: 25.001,
                    overallLength: 150.01
                },
                {
                    timestamp: new Date(Date.now() - 10800000),
                    operator: 'David Chen',
                    serialNumber: 'P003',
                    boreDiameter: 24.999,
                    overallLength: 149.99
                }
            ];

            // Start live updates for metrics
            this.startMetricsUpdates();
        }

        /**
         * Start periodic metrics updates
         */
        startMetricsUpdates() {
            if (this.metricsUpdateInterval) {
                clearInterval(this.metricsUpdateInterval);
            }

            this.metricsUpdateInterval = setInterval(() => {
                const metricsCards = document.querySelectorAll('.metric-value');
                metricsCards.forEach(card => {
                    if (card.textContent.includes('%') && Math.random() < 0.2) {
                        const currentValue = parseInt(card.textContent);
                        const newValue = Math.max(70, Math.min(98, currentValue + (Math.random() - 0.5) * 2));
                        card.textContent = Math.round(newValue) + '%';
                    }
                });
            }, 10000);
        }

        /**
         * Show loading indicator
         */
        showLoading(show) {
            const indicator = document.getElementById('loadingIndicator');
            if (!indicator) return;

            if (show) {
                indicator.classList.remove('hidden');
            } else {
                indicator.classList.add('hidden');
            }
        }

        /**
         * Show error message
         */
        showError(message) {
            alert(message); // In production, replace with a better notification system
            console.error(message);
        }

        /**
         * Show notification
         */
        showNotification(message, type = 'info') {
            alert(message); // In production, replace with a better notification system
            console.log(`[${type}] ${message}`);
        }

        /**
         * Escape HTML to prevent XSS
         */
        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        /**
         * Cleanup
         */
        destroy() {
            if (this.productionMonitoringInterval) {
                clearInterval(this.productionMonitoringInterval);
            }
            if (this.metricsUpdateInterval) {
                clearInterval(this.metricsUpdateInterval);
            }
        }
    }

    // Initialize app when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.manufacturingApp = new ManufacturingApp();
        });
    } else {
        window.manufacturingApp = new ManufacturingApp();
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (window.manufacturingApp) {
            window.manufacturingApp.destroy();
        }
    });

})();
