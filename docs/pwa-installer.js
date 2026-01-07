// MOFNet PWA Installer
class MOFNetPWA {
  constructor() {
    this.deferredPrompt = null;
    this.isPWA = window.matchMedia('(display-mode: standalone)').matches;
    this.init();
  }

  init() {
    // Listen for install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallButton();
    });

    // Check if already installed
    if (this.isPWA) {
      console.log('MOFNet is running as PWA');
    }
  }

  showInstallButton() {
    // Create install button
    const installBtn = document.createElement('button');
    installBtn.id = 'pwa-install-btn';
    installBtn.innerHTML = '📱 Install MOFNet App';
    installBtn.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #003399;
      color: white;
      padding: 12px 24px;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      cursor: pointer;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0, 51, 153, 0.3);
    `;
    
    installBtn.onclick = () => this.installApp();
    document.body.appendChild(installBtn);

    // Auto-hide after 30 seconds
    setTimeout(() => {
      if (document.getElementById('pwa-install-btn')) {
        installBtn.style.display = 'none';
      }
    }, 30000);
  }

  async installApp() {
    if (!this.deferredPrompt) return;
    
    this.deferredPrompt.prompt();
    const { outcome } = await this.deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
      console.log('MOFNet PWA installed successfully');
      const btn = document.getElementById('pwa-install-btn');
      if (btn) btn.remove();
    }
    
    this.deferredPrompt = null;
  }

  // Check PWA capabilities
  static checkSupport() {
    return {
      serviceWorker: 'serviceWorker' in navigator,
      installPrompt: 'beforeinstallprompt' in window,
      standalone: window.matchMedia('(display-mode: standalone)').matches,
      storage: 'caches' in window
    };
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.mofnetPWA = new MOFNetPWA();
  
  // Log PWA support
  const support = MOFNetPWA.checkSupport();
  console.log('PWA Support:', support);
});
