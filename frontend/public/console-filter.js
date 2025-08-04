/**
 * 控制台过滤器 - 专门处理浏览器原生输出的弃用警告
 * 这些警告不通过JavaScript console方法输出，而是浏览器内核直接输出
 */

(function() {
  'use strict';
  
  // 创建一个自定义的console对象来替换原生console
  const originalConsole = window.console;
  
  // 创建过滤后的console方法
  function createFilteredConsoleMethod(methodName) {
    const originalMethod = originalConsole[methodName];
    
    return function(...args) {
      // 检查是否包含需要过滤的内容
      const message = args.join(' ');
      
      const shouldFilter = [
        'Deprecation',
        'DOMNodeInsertedIntoDocument',
        'DOM Mutation Event',
        'deprecated',
        'legacy-event-types',
        'synchronous'
      ].some(keyword => 
        message.toLowerCase().includes(keyword.toLowerCase())
      );
      
      // 如果不需要过滤，则正常输出
      if (!shouldFilter) {
        return originalMethod.apply(originalConsole, args);
      }
      
      // 过滤的消息可以选择性地输出到debug
      if (window._showFilteredWarnings) {
        originalConsole.debug('🔇 已过滤警告:', message);
      }
    };
  }
  
  // 只重写console.warn，保留其他方法的正常功能
  if (originalConsole.warn) {
    window.console.warn = createFilteredConsoleMethod('warn');
  }

  // 保留error、log等方法的原始功能，避免干扰Vue等框架
  
  // 尝试拦截浏览器原生的警告输出
  try {
    // 重写window.onerror来捕获更多错误
    const originalOnError = window.onerror;
    window.onerror = function(message, source, lineno, colno, error) {
      if (typeof message === 'string') {
        const shouldFilter = [
          'Deprecation',
          'DOMNodeInsertedIntoDocument',
          'DOM Mutation Event'
        ].some(keyword => message.includes(keyword));
        
        if (shouldFilter) {
          console.debug('🔇 已过滤onerror警告:', message);
          return true; // 阻止默认错误处理
        }
      }
      
      if (originalOnError) {
        return originalOnError.call(this, message, source, lineno, colno, error);
      }
      return false;
    };
    
    // 监听unhandledrejection事件
    window.addEventListener('unhandledrejection', function(event) {
      if (event.reason && typeof event.reason === 'string') {
        const shouldFilter = [
          'Deprecation',
          'DOMNodeInsertedIntoDocument'
        ].some(keyword => event.reason.includes(keyword));
        
        if (shouldFilter) {
          console.debug('🔇 已过滤unhandledrejection警告:', event.reason);
          event.preventDefault();
        }
      }
    });
    
  } catch (e) {
    console.debug('控制台过滤器初始化部分失败:', e);
  }
  
  // 尝试使用MutationObserver监控控制台DOM变化（如果在开发者工具中）
  try {
    if (typeof MutationObserver !== 'undefined') {
      const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
          if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(function(node) {
              if (node.nodeType === Node.TEXT_NODE || node.nodeType === Node.ELEMENT_NODE) {
                const text = node.textContent || node.innerText || '';
                if (text.includes('DOMNodeInsertedIntoDocument') || 
                    text.includes('Deprecation') ||
                    text.includes('DOM Mutation Event')) {
                  // 尝试隐藏或移除这个节点
                  try {
                    if (node.parentNode) {
                      node.parentNode.removeChild(node);
                      console.debug('🔇 已移除DOM中的弃用警告节点');
                    }
                  } catch (e) {
                    // 移除失败，尝试隐藏
                    try {
                      if (node.style) {
                        node.style.display = 'none';
                      }
                    } catch (e2) {
                      // 隐藏也失败，忽略
                    }
                  }
                }
              }
            });
          }
        });
      });
      
      // 观察document的变化
      if (document.body) {
        observer.observe(document.body, {
          childList: true,
          subtree: true,
          characterData: true
        });
      } else {
        document.addEventListener('DOMContentLoaded', function() {
          observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true
          });
        });
      }
    }
  } catch (e) {
    console.debug('MutationObserver过滤器初始化失败:', e);
  }
  
  // 添加一个全局方法来切换过滤显示
  window.toggleFilteredWarnings = function() {
    window._showFilteredWarnings = !window._showFilteredWarnings;
    console.log(`🔇 过滤警告显示: ${window._showFilteredWarnings ? '开启' : '关闭'}`);
  };
  
  console.log('🔇 控制台过滤器已加载');
  
})();
