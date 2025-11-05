# Deployment Guide

This guide covers various deployment options for the Jaque.ai Manufacturing Operations Platform.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Static Hosting](#static-hosting)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Platforms](#cloud-platforms)
6. [CDN Integration](#cdn-integration)
7. [SSL/TLS Setup](#ssltls-setup)
8. [Environment Configuration](#environment-configuration)

## Prerequisites

- Modern web browser
- Git (for version control)
- Text editor or IDE
- HTTP server (for local development)

## Local Development

### Option 1: Python HTTP Server

**Python 3.x:**
```bash
cd manufacturing
python3 -m http.server 8000
```

**Python 2.x:**
```bash
cd manufacturing
python -m SimpleHTTPServer 8000
```

Access at: `http://localhost:8000`

### Option 2: Node.js HTTP Server

```bash
npx http-server manufacturing -p 8000
```

### Option 3: PHP Built-in Server

```bash
cd manufacturing
php -S localhost:8000
```

## Static Hosting

### GitHub Pages

1. **Enable GitHub Pages:**
   - Go to repository Settings
   - Navigate to Pages section
   - Select branch and `/manufacturing` folder
   - Click Save

2. **Access your site:**
   ```
   https://youhannam.github.io/Jaque-landing-page/manufacturing/
   ```

### Netlify

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Deploy:**
   ```bash
   cd manufacturing
   netlify deploy --prod
   ```

3. **Or use drag-and-drop:**
   - Visit https://app.netlify.com/drop
   - Drag the `manufacturing` folder

### Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd manufacturing
   vercel --prod
   ```

### AWS S3 + CloudFront

1. **Create S3 Bucket:**
   ```bash
   aws s3 mb s3://your-bucket-name
   ```

2. **Configure for static website:**
   ```bash
   aws s3 website s3://your-bucket-name --index-document index.html
   ```

3. **Upload files:**
   ```bash
   aws s3 sync . s3://your-bucket-name/ --acl public-read
   ```

4. **Setup CloudFront distribution** (optional but recommended)

## Docker Deployment

### Using Project's Docker Setup

From the project root:

```bash
docker-compose up -d
```

### Custom Nginx Container

1. **Create Dockerfile:**
   ```dockerfile
   FROM nginx:alpine
   COPY manufacturing/ /usr/share/nginx/html/
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Build and run:**
   ```bash
   docker build -t manufacturing-platform .
   docker run -d -p 80:80 manufacturing-platform
   ```

## Cloud Platforms

### Google Cloud Platform (GCS)

1. **Create bucket:**
   ```bash
   gsutil mb gs://your-bucket-name
   ```

2. **Upload files:**
   ```bash
   gsutil -m cp -r manufacturing/* gs://your-bucket-name/
   ```

3. **Make public:**
   ```bash
   gsutil iam ch allUsers:objectViewer gs://your-bucket-name
   ```

### Azure Static Web Apps

1. **Install Azure CLI:**
   ```bash
   az login
   ```

2. **Create Static Web App:**
   ```bash
   az staticwebapp create \
     --name manufacturing-platform \
     --resource-group your-resource-group \
     --source manufacturing \
     --location "eastus2"
   ```

### DigitalOcean App Platform

1. **Create app.yaml:**
   ```yaml
   name: manufacturing-platform
   static_sites:
   - name: web
     build_command: echo "No build needed"
     output_dir: manufacturing
     routes:
     - path: /
   ```

2. **Deploy via CLI or web interface**

## CDN Integration

### Cloudflare

1. **Add site to Cloudflare**
2. **Update nameservers**
3. **Configure caching rules:**
   - Cache static assets
   - Set appropriate TTL
   - Enable Auto Minify for HTML, CSS, JS

### AWS CloudFront

```bash
aws cloudfront create-distribution \
  --origin-domain-name your-bucket.s3.amazonaws.com \
  --default-root-object index.html
```

## SSL/TLS Setup

### Let's Encrypt (with Nginx)

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Cloudflare SSL

- Automatic with Cloudflare proxy
- Choose SSL mode: Flexible, Full, or Full (strict)

## Environment Configuration

### Production Checklist

- [ ] Remove console.log statements (or use environment-based logging)
- [ ] Enable CSP headers
- [ ] Configure CORS if needed
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure analytics (Google Analytics, etc.)
- [ ] Minify CSS and JavaScript
- [ ] Optimize images
- [ ] Enable gzip/brotli compression
- [ ] Set proper cache headers
- [ ] Configure 404 and error pages
- [ ] Set up monitoring and uptime checks
- [ ] Configure backup strategy
- [ ] Document API endpoints (if using backend)
- [ ] Set up CI/CD pipeline

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/manufacturing;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/css application/javascript application/json;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Apache Configuration Example

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /var/www/manufacturing

    <Directory /var/www/manufacturing>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Compression
    <IfModule mod_deflate.c>
        AddOutputFilterByType DEFLATE text/html text/css application/javascript
    </IfModule>

    # Cache control
    <IfModule mod_expires.c>
        ExpiresActive On
        ExpiresByType text/css "access plus 1 year"
        ExpiresByType application/javascript "access plus 1 year"
        ExpiresByType image/png "access plus 1 year"
    </IfModule>
</VirtualHost>
```

## Performance Optimization

### Content Delivery

1. **Use a CDN** for static assets
2. **Enable compression** (gzip/brotli)
3. **Set cache headers** appropriately
4. **Optimize images** before deployment
5. **Minify CSS/JS** for production

### Monitoring

**Recommended tools:**
- Google PageSpeed Insights
- WebPageTest
- Lighthouse CI
- New Relic / Datadog
- UptimeRobot / Pingdom

## Rollback Strategy

### Quick Rollback

**Git-based:**
```bash
git revert HEAD
git push origin main
```

**S3 versioning:**
```bash
aws s3api list-object-versions --bucket your-bucket
aws s3api get-object --bucket your-bucket --key index.html --version-id <version-id>
```

### Blue-Green Deployment

Maintain two identical environments:
1. Deploy to "green" environment
2. Test thoroughly
3. Switch traffic from "blue" to "green"
4. Keep "blue" for quick rollback

## Troubleshooting

### Common Issues

**404 Errors:**
- Check file paths are correct
- Verify index.html exists
- Configure server for SPA routing

**CORS Errors:**
- Add CORS headers if using APIs
- Check CSP configuration

**Loading Slowly:**
- Enable compression
- Use CDN
- Optimize assets
- Check server resources

**Not Mobile Responsive:**
- Verify viewport meta tag
- Test on multiple devices
- Use browser dev tools

## Security Best Practices

1. **Use HTTPS** everywhere
2. **Set security headers:**
   - Content-Security-Policy
   - X-Frame-Options
   - X-Content-Type-Options
   - X-XSS-Protection
3. **Keep dependencies updated**
4. **Sanitize all inputs**
5. **Regular security audits**
6. **Monitor for vulnerabilities**
7. **Implement rate limiting** (if using API)
8. **Use environment variables** for sensitive data

## Continuous Integration / Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy Manufacturing Platform

on:
  push:
    branches: [ main ]
    paths:
      - 'manufacturing/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Deploy to Netlify
        uses: netlify/actions/cli@master
        with:
          args: deploy --dir=manufacturing --prod
        env:
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```

## Support

For deployment issues or questions:
- Check the main README.md
- Open an issue on GitHub
- Contact: support@jaque.ai

---

**Last Updated:** November 2025
**Version:** 1.0.0
