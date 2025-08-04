/**
 * 简单安全的警告过滤器
 * 只过滤明确的DOM弃用警告，不干扰其他功能
 */

(function() {
  'use strict';
  
  // 保存原始的console.warn方法
  const originalWarn = console.warn;
  
  // 需要过滤的特定警告关键词
  const FILTER_KEYWORDS = [
    'DOMNodeInsertedIntoDocument',
    'DOM Mutation Event',
    'legacy-event-types'
  ];
  
  // 重写console.warn方法（安全版本）
  console.warn = function(...args) {
    try {
      // 安全地转换参数为字符串
      const message = args.map(arg => {
        if (arg === null) return 'null';
        if (arg === undefined) return 'undefined';
        if (typeof arg === 'object') {
          try {
            return JSON.stringify(arg);
          } catch (e) {
            return '[Object]';
          }
        }
        return String(arg);
      }).join(' ');

      // 检查是否包含需要过滤的关键词
      const shouldFilter = FILTER_KEYWORDS.some(keyword =>
        message.includes(keyword)
      );

      if (shouldFilter) {
        // 过滤掉DOM弃用警告，但在debug中记录
        console.debug('🔇 已过滤DOM弃用警告');
        return;
      }

      // 其他警告正常输出
      originalWarn.apply(console, args);
    } catch (e) {
      // 如果处理失败，直接调用原始方法
      originalWarn.apply(console, args);
    }
  };
  
  // 简单的addEventListener拦截（仅记录，不阻止）
  if (typeof EventTarget !== 'undefined') {
    const originalAddEventListener = EventTarget.prototype.addEventListener;
    
    EventTarget.prototype.addEventListener = function(type, listener, options) {
      // 弃用的DOM事件列表
      const deprecatedEvents = [
        'DOMNodeInsertedIntoDocument',
        'DOMNodeInserted',
        'DOMNodeRemoved'
      ];
      
      if (deprecatedEvents.includes(type)) {
        console.debug(`🔇 检测到弃用DOM事件监听器: ${type}`);
        // 仍然允许添加，但记录下来
      }
      
      // 正常处理所有事件
      return originalAddEventListener.call(this, type, listener, options);
    };
  }
  
  console.log('🔇 简单警告过滤器已加载');
  
})();
