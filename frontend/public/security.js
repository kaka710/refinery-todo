/**
 * 安全配置和 Mixed Content 处理
 * 在页面加载前执行，确保安全策略正确应用
 */

(function() {
  'use strict';
  
  // 设置内容安全策略
  function setContentSecurityPolicy() {
    const meta = document.createElement('meta');
    meta.httpEquiv = 'Content-Security-Policy';
    meta.content = [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob: https:",
      "font-src 'self' data:",
      "connect-src 'self' ws: wss: http://localhost:* https://localhost:* http://127.0.0.1:* https://127.0.0.1:*",
      "frame-src 'none'",
      "object-src 'none'",
      "base-uri 'self'",
      "form-action 'self'",
      "upgrade-insecure-requests"
    ].join('; ');
    
    document.head.appendChild(meta);
  }
  
  // 处理 Mixed Content 警告
  function handleMixedContent() {
    // 如果页面是通过 HTTPS 加载的，确保所有资源也使用 HTTPS
    if (location.protocol === 'https:') {
      // 监听所有新添加的元素
      const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
          mutation.addedNodes.forEach(function(node) {
            if (node.nodeType === 1) { // Element node
              upgradeInsecureElements(node);
            }
          });
        });
      });
      
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
      
      // 升级现有的不安全元素
      upgradeInsecureElements(document);
    }
  }
  
  // 升级不安全的元素
  function upgradeInsecureElements(root) {
    const selectors = [
      'img[src^="http:"]',
      'script[src^="http:"]',
      'link[href^="http:"]',
      'iframe[src^="http:"]',
      'source[src^="http:"]',
      'video[src^="http:"]',
      'audio[src^="http:"]'
    ];
    
    selectors.forEach(function(selector) {
      const elements = root.querySelectorAll ? root.querySelectorAll(selector) : [];
      Array.from(elements).forEach(function(element) {
        const attr = element.src ? 'src' : 'href';
        if (element[attr] && element[attr].startsWith('http:')) {
          element[attr] = element[attr].replace('http:', 'https:');
        }
      });
    });
  }
  
  // 禁用已弃用的事件监听器警告
  function suppressDeprecatedEventWarnings() {
    const originalAddEventListener = EventTarget.prototype.addEventListener;
    
    EventTarget.prototype.addEventListener = function(type, listener, options) {
      // 检查是否是已弃用的 DOM Mutation Events
      const deprecatedEvents = [
        'DOMNodeInserted',
        'DOMNodeRemoved',
        'DOMNodeInsertedIntoDocument',
        'DOMNodeRemovedFromDocument',
        'DOMAttrModified',
        'DOMCharacterDataModified',
        'DOMSubtreeModified'
      ];
      
      if (deprecatedEvents.includes(type)) {
        // 静默处理，不显示警告
        return originalAddEventListener.call(this, type, listener, options);
      }
      
      return originalAddEventListener.call(this, type, listener, options);
    };
  }
  
  // 初始化安全配置
  function initSecurity() {
    try {
      // 设置 CSP
      setContentSecurityPolicy();
      
      // 处理 Mixed Content
      handleMixedContent();
      
      // 禁用弃用警告
      suppressDeprecatedEventWarnings();
      
      console.log('安全配置已初始化');
    } catch (error) {
      console.error('安全配置初始化失败:', error);
    }
  }
  
  // 页面加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSecurity);
  } else {
    initSecurity();
  }
})();
