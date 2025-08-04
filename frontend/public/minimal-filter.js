/**
 * 最小化警告过滤器
 * 不重写console方法，只阻止DOM事件监听器
 */

(function() {
  'use strict';
  
  // 弃用的DOM事件列表
  const DEPRECATED_EVENTS = [
    'DOMNodeInsertedIntoDocument',
    'DOMNodeInserted',
    'DOMNodeRemoved',
    'DOMAttrModified',
    'DOMCharacterDataModified',
    'DOMSubtreeModified'
  ];
  
  // 只重写addEventListener，不重写console方法
  if (typeof EventTarget !== 'undefined') {
    const originalAddEventListener = EventTarget.prototype.addEventListener;
    
    EventTarget.prototype.addEventListener = function(type, listener, options) {
      if (DEPRECATED_EVENTS.includes(type)) {
        // 静默忽略弃用的DOM事件监听器
        console.debug(`🔇 已阻止弃用的DOM事件监听器: ${type}`);
        return;
      }
      
      // 正常事件继续处理
      return originalAddEventListener.call(this, type, listener, options);
    };
  }
  
  // 添加CSS样式来隐藏开发者工具中的特定警告（实验性）
  try {
    const style = document.createElement('style');
    style.textContent = `
      /* 尝试隐藏开发者工具中的弃用警告 */
      .console-warning-level[data-text*="Deprecation"],
      .console-warning-level[data-text*="DOMNodeInsertedIntoDocument"] {
        display: none !important;
      }
    `;
    if (document.head) {
      document.head.appendChild(style);
    } else {
      document.addEventListener('DOMContentLoaded', function() {
        document.head.appendChild(style);
      });
    }
  } catch (e) {
    // CSS方法可能不起作用，忽略错误
  }
  
  console.log('🔇 最小化警告过滤器已加载（不重写console方法）');
  
})();
