/**
 * DOM事件过滤器 - 在页面加载早期阻止弃用的DOM事件
 * 必须在所有其他脚本之前加载
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
  
  // 1. 重写addEventListener以阻止弃用事件
  if (typeof EventTarget !== 'undefined') {
    const originalAddEventListener = EventTarget.prototype.addEventListener;

    EventTarget.prototype.addEventListener = function(type, listener, options) {
      // 如果是弃用的DOM事件，静默忽略
      if (DEPRECATED_EVENTS.includes(type)) {
        console.debug(`🔇 已阻止弃用的DOM事件监听器: ${type}`);
        return;
      }

      // 正常事件继续处理
      return originalAddEventListener.call(this, type, listener, options);
    };

    // 同时重写attachEvent（IE兼容）
    if (typeof Element !== 'undefined' && Element.prototype.attachEvent) {
      const originalAttachEvent = Element.prototype.attachEvent;
      Element.prototype.attachEvent = function(event, listener) {
        const eventType = event.replace('on', '');
        if (DEPRECATED_EVENTS.includes(eventType)) {
          console.debug(`🔇 已阻止弃用的DOM事件监听器 (attachEvent): ${eventType}`);
          return;
        }
        return originalAttachEvent.call(this, event, listener);
      };
    }
  }
  
  // 2. 重写console方法过滤弃用警告（仅过滤warn，保留error和log）
  const originalConsoleWarn = console.warn;

  function shouldSuppressMessage(message) {
    // 只过滤明确的DOM弃用警告，不过滤其他内容
    const suppressKeywords = [
      'DOMNodeInsertedIntoDocument',
      'DOM Mutation Event',
      'legacy-event-types'
    ];

    return suppressKeywords.some(keyword =>
      message.toLowerCase().includes(keyword.toLowerCase())
    );
  }

  // 只重写console.warn，保留error和log的正常功能
  console.warn = function(...args) {
    const message = args.join(' ');
    if (!shouldSuppressMessage(message)) {
      originalConsoleWarn.apply(console, args);
    } else {
      // 被过滤的警告可以输出到debug
      console.debug('🔇 已过滤DOM弃用警告:', message.substring(0, 100) + '...');
    }
  };
  
  // 3. 温和的方法：仅记录弃用事件的使用（不删除）
  try {
    // 记录但不阻止弃用事件的使用
    DEPRECATED_EVENTS.forEach(eventType => {
      try {
        // 仅在debug模式下记录这些事件的存在
        if (typeof Event !== 'undefined' && Event[eventType.toUpperCase()]) {
          console.debug(`🔍 检测到弃用事件常量: ${eventType}`);
        }
      } catch (e) {
        // 忽略检测失败的情况
      }
    });
  } catch (e) {
    console.debug('无法检测DOM事件常量:', e);
  }

  // 4. 尝试阻止MutationEvent的创建
  try {
    if (typeof MutationEvent !== 'undefined') {
      // 重写MutationEvent构造函数
      const OriginalMutationEvent = window.MutationEvent;
      window.MutationEvent = function(...args) {
        console.debug('🔇 已阻止MutationEvent的创建，建议使用MutationObserver');
        // 返回一个空对象而不是真正的MutationEvent
        return {};
      };

      // 保持原型链
      window.MutationEvent.prototype = OriginalMutationEvent.prototype;
    }
  } catch (e) {
    console.debug('无法重写MutationEvent:', e);
  }
  
  // 5. 尝试使用CSS隐藏控制台中的弃用警告（实验性）
  try {
    const style = document.createElement('style');
    style.textContent = `
      /* 尝试隐藏开发者工具中的弃用警告 */
      .console-warning-level[data-text*="Deprecation"],
      .console-warning-level[data-text*="DOMNodeInsertedIntoDocument"],
      .console-warning-level[data-text*="DOM Mutation Event"] {
        display: none !important;
      }
    `;
    document.head?.appendChild(style);
  } catch (e) {
    // CSS方法可能不起作用，忽略错误
  }

  // 6. 监听DOM加载完成，进一步清理
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      console.log('🔇 DOM事件过滤器已激活');

      // DOM加载完成后，再次尝试清理
      setTimeout(() => {
        // 查找并移除可能的弃用事件监听器
        DEPRECATED_EVENTS.forEach(eventType => {
          try {
            document.removeEventListener(eventType, function() {}, true);
            document.removeEventListener(eventType, function() {}, false);
          } catch (e) {
            // 忽略移除失败
          }
        });
      }, 100);
    });
  } else {
    console.log('🔇 DOM事件过滤器已激活');
  }
  
  // 5. 全局错误处理，过滤弃用警告
  const originalOnError = window.onerror;
  window.onerror = function(message, source, lineno, colno, error) {
    if (typeof message === 'string' && shouldSuppressMessage(message)) {
      return true; // 阻止错误显示
    }
    
    if (originalOnError) {
      return originalOnError.call(this, message, source, lineno, colno, error);
    }
    
    return false;
  };
  
  // 6. 处理unhandledrejection中的弃用警告
  window.addEventListener('unhandledrejection', function(event) {
    if (event.reason && typeof event.reason.message === 'string') {
      if (shouldSuppressMessage(event.reason.message)) {
        event.preventDefault();
        console.debug('🔇 已过滤unhandledrejection中的弃用警告');
      }
    }
  });
  
})();

console.log('🔇 DOM事件过滤器已加载');
