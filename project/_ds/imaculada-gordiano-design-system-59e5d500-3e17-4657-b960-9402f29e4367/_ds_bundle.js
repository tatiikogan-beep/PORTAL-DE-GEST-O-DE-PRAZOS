/* @ds-bundle: {"format":3,"namespace":"ImaculadaGordianoDesignSystem_59e5d5","components":[{"name":"Avatar","sourcePath":"components/core/Avatar.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"IconButton","sourcePath":"components/core/IconButton.jsx"},{"name":"Badge","sourcePath":"components/display/Badge.jsx"},{"name":"StatusDot","sourcePath":"components/display/StatusDot.jsx"},{"name":"Tabs","sourcePath":"components/display/Tabs.jsx"},{"name":"Tag","sourcePath":"components/display/Tag.jsx"},{"name":"Toast","sourcePath":"components/feedback/Toast.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"}],"sourceHashes":{"components/core/Avatar.jsx":"4395f8e6edc5","components/core/Button.jsx":"fe0249bf0a87","components/core/Card.jsx":"6d7fe896ba6e","components/core/IconButton.jsx":"3409a810b8cf","components/display/Badge.jsx":"4b4add9de8f6","components/display/StatusDot.jsx":"5832a88a2806","components/display/Tabs.jsx":"d091ef6f51ae","components/display/Tag.jsx":"ae4eaf5aa5fd","components/feedback/Toast.jsx":"7bd59d9d0c55","components/forms/Input.jsx":"1d99ba313b6c","components/forms/Select.jsx":"ce05d162ff7d","ui_kits/dashboard/CorrespondentesPanel.jsx":"c302ca31e0a6","ui_kits/dashboard/FinanceiroPanel.jsx":"609dbd26d7b6","ui_kits/dashboard/Header.jsx":"ac9b927ac101","ui_kits/dashboard/Panels.jsx":"c8dac0fe2e4b"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.ImaculadaGordianoDesignSystem_59e5d5 = window.ImaculadaGordianoDesignSystem_59e5d5 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Avatar.jsx
try { (() => {
function Avatar({
  name = '',
  src,
  size = 'md',
  crest = false,
  style
}) {
  const px = size === 'sm' ? 28 : size === 'lg' ? 48 : 36;
  const initials = name.trim().split(/\s+/).slice(0, 2).map(w => w[0]).join('').toUpperCase();
  const base = {
    width: px,
    height: px,
    borderRadius: '50%',
    overflow: 'hidden',
    flex: 'none',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'var(--font-sans)',
    fontWeight: 600,
    fontSize: px * 0.38,
    background: crest ? 'var(--surface-card)' : 'var(--wine-600)',
    color: 'var(--gold-100)',
    border: crest ? '1px solid var(--border-soft)' : '1px solid transparent',
    ...style
  };
  if (src || crest) {
    return /*#__PURE__*/React.createElement("span", {
      style: base
    }, /*#__PURE__*/React.createElement("img", {
      src: src || resolveCrest(),
      alt: name || 'Imaculada Gordiano',
      style: {
        width: '100%',
        height: '100%',
        objectFit: 'cover'
      }
    }));
  }
  return /*#__PURE__*/React.createElement("span", {
    style: base,
    title: name
  }, initials || '·');
}
function resolveCrest() {
  // crest asset lives at <project root>/assets/crest.png; pages at any depth can override via data attr
  const el = document.querySelector('[data-ds-root]');
  const root = el ? el.getAttribute('data-ds-root') : '.';
  return root.replace(/\/$/, '') + '/assets/crest.png';
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const sizes = {
  sm: {
    padding: '7px 14px',
    fontSize: '12px'
  },
  md: {
    padding: '10px 20px',
    fontSize: '14px'
  },
  lg: {
    padding: '13px 26px',
    fontSize: '15px'
  }
};
const variants = {
  primary: {
    base: {
      background: 'var(--wine-600)',
      color: 'var(--gold-100)',
      border: '1px solid transparent',
      boxShadow: 'var(--shadow-wine)'
    },
    hover: {
      background: 'var(--wine-700)'
    },
    active: {
      background: 'var(--wine-800)',
      boxShadow: 'none'
    }
  },
  accent: {
    base: {
      background: 'var(--gold-400)',
      color: 'var(--wine-800)',
      border: '1px solid transparent',
      boxShadow: 'var(--shadow-sm)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--ls-wider)',
      fontWeight: 600
    },
    hover: {
      background: 'var(--gold-500)'
    },
    active: {
      background: 'var(--gold-600)',
      boxShadow: 'none'
    }
  },
  secondary: {
    base: {
      background: 'var(--surface-card)',
      color: 'var(--wine-600)',
      border: '1px solid var(--border-soft)',
      boxShadow: 'var(--shadow-xs)'
    },
    hover: {
      background: 'var(--sand-50)',
      borderColor: 'var(--border-strong)'
    },
    active: {
      background: 'var(--sand-200)'
    }
  },
  ghost: {
    base: {
      background: 'transparent',
      color: 'var(--wine-600)',
      border: '1px solid transparent'
    },
    hover: {
      background: 'var(--wine-50)'
    },
    active: {
      background: 'var(--wine-100)'
    }
  }
};
function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  icon = null,
  children,
  style,
  ...rest
}) {
  const [state, setState] = React.useState('base');
  const v = variants[variant] || variants.primary;
  const s = sizes[size] || sizes.md;
  const merged = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    fontFamily: 'var(--font-sans)',
    fontWeight: 600,
    lineHeight: 1,
    borderRadius: 'var(--radius-md)',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'background var(--dur-base) var(--ease-standard), box-shadow var(--dur-base) var(--ease-standard)',
    opacity: disabled ? 0.45 : 1,
    ...s,
    ...v.base,
    ...(!disabled && state === 'hover' ? v.hover : {}),
    ...(!disabled && state === 'active' ? v.active : {}),
    ...style
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    disabled: disabled,
    style: merged,
    onMouseEnter: () => setState('hover'),
    onMouseLeave: () => setState('base'),
    onMouseDown: () => setState('active'),
    onMouseUp: () => setState('hover')
  }, rest), icon, children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Card({
  kicker,
  title,
  icon,
  status,
  footer,
  hoverable = false,
  children,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      position: 'relative',
      background: 'var(--surface-card)',
      border: 'var(--card-border)',
      borderRadius: 'var(--card-radius)',
      boxShadow: hoverable && hover ? 'var(--shadow-md)' : 'var(--card-shadow)',
      padding: 'var(--card-pad)',
      fontFamily: 'var(--font-sans)',
      transition: 'box-shadow var(--dur-base) var(--ease-standard), background var(--dur-base) var(--ease-standard)',
      ...(hoverable && hover ? {
        background: 'var(--sand-50)',
        cursor: 'pointer'
      } : {}),
      ...style
    },
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false)
  }, rest), status ? /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      top: 14,
      right: 14,
      width: 9,
      height: 9,
      borderRadius: '50%',
      background: status === 'active' ? 'var(--green-500)' : status === 'warning' ? 'var(--gold-400)' : 'var(--sand-400)'
    }
  }) : null, icon ? /*#__PURE__*/React.createElement("div", {
    style: {
      width: 38,
      height: 38,
      borderRadius: 'var(--radius-md)',
      background: 'var(--rose-soft)',
      color: 'var(--wine-600)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: 12
    }
  }, icon) : null, kicker ? /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      letterSpacing: 'var(--ls-wider)',
      textTransform: 'uppercase',
      color: 'var(--text-category)',
      fontWeight: 600,
      marginBottom: 4
    }
  }, kicker) : null, title ? /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: '0 0 8px',
      fontSize: 'var(--fs-xl)',
      fontWeight: 600,
      color: 'var(--text-strong)',
      lineHeight: 'var(--lh-snug)'
    }
  }, title) : null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--fs-sm)',
      color: 'var(--text-body)',
      lineHeight: 'var(--lh-normal)'
    }
  }, children), footer ? /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14,
      paddingTop: 12,
      borderTop: '1px solid var(--border-soft)',
      fontSize: 'var(--fs-xs)',
      color: 'var(--text-muted)'
    }
  }, footer) : null);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function IconButton({
  label,
  size = 'md',
  variant = 'neutral',
  disabled = false,
  children,
  style,
  ...rest
}) {
  const [state, setState] = React.useState('base');
  const px = size === 'sm' ? 30 : size === 'lg' ? 44 : 36;
  const palettes = {
    neutral: {
      base: {
        background: 'transparent',
        color: 'var(--ink-500)',
        border: '1px solid transparent'
      },
      hover: {
        background: 'var(--sand-200)',
        color: 'var(--ink-700)'
      },
      active: {
        background: 'var(--sand-300)'
      }
    },
    wine: {
      base: {
        background: 'var(--rose-soft)',
        color: 'var(--wine-600)',
        border: '1px solid transparent'
      },
      hover: {
        background: 'var(--wine-100)'
      },
      active: {
        background: 'var(--wine-200)'
      }
    },
    outline: {
      base: {
        background: 'var(--surface-card)',
        color: 'var(--wine-600)',
        border: '1px solid var(--border-soft)'
      },
      hover: {
        background: 'var(--sand-50)',
        borderColor: 'var(--border-strong)'
      },
      active: {
        background: 'var(--sand-200)'
      }
    }
  };
  const v = palettes[variant] || palettes.neutral;
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    "aria-label": label,
    title: label,
    disabled: disabled,
    style: {
      width: px,
      height: px,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 'var(--radius-md)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'background var(--dur-fast) var(--ease-standard)',
      opacity: disabled ? 0.45 : 1,
      ...v.base,
      ...(!disabled && state === 'hover' ? v.hover : {}),
      ...(!disabled && state === 'active' ? v.active : {}),
      ...style
    },
    onMouseEnter: () => setState('hover'),
    onMouseLeave: () => setState('base'),
    onMouseDown: () => setState('active'),
    onMouseUp: () => setState('hover')
  }, rest), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/display/Badge.jsx
try { (() => {
const tones = {
  success: {
    bg: 'var(--green-100)',
    fg: 'var(--green-700)',
    dot: 'var(--green-500)'
  },
  warning: {
    bg: 'var(--gold-50)',
    fg: 'var(--gold-600)',
    dot: 'var(--gold-400)'
  },
  danger: {
    bg: 'var(--wine-50)',
    fg: 'var(--wine-600)',
    dot: 'var(--wine-500)'
  },
  neutral: {
    bg: 'var(--sand-200)',
    fg: 'var(--ink-700)',
    dot: 'var(--ink-400)'
  }
};
function Badge({
  tone = 'neutral',
  dot = false,
  children,
  style
}) {
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      background: t.bg,
      color: t.fg,
      borderRadius: 'var(--radius-pill)',
      padding: '3px 10px',
      fontFamily: 'var(--font-sans)',
      fontSize: 12,
      fontWeight: 500,
      lineHeight: 1.4,
      ...style
    }
  }, dot ? /*#__PURE__*/React.createElement("span", {
    style: {
      width: 7,
      height: 7,
      borderRadius: '50%',
      background: t.dot,
      flex: 'none'
    }
  }) : null, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Badge.jsx", error: String((e && e.message) || e) }); }

// components/display/StatusDot.jsx
try { (() => {
function StatusDot({
  tone = 'active',
  pulse = false,
  size = 9,
  style
}) {
  const colors = {
    active: 'var(--green-500)',
    warning: 'var(--gold-400)',
    danger: 'var(--wine-500)',
    idle: 'var(--sand-400)'
  };
  return /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      display: 'inline-flex',
      width: size,
      height: size,
      flex: 'none',
      ...style
    }
  }, pulse ? /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      borderRadius: '50%',
      background: colors[tone],
      opacity: 0.5,
      animation: 'igsa-dot-pulse 2s var(--ease-standard) infinite'
    }
  }) : null, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      width: '100%',
      height: '100%',
      borderRadius: '50%',
      background: colors[tone] || colors.active
    }
  }), /*#__PURE__*/React.createElement("style", null, '@keyframes igsa-dot-pulse { 0% { transform: scale(1); opacity: 0.5; } 70% { transform: scale(2.1); opacity: 0; } 100% { transform: scale(2.1); opacity: 0; } } @media (prefers-reduced-motion: reduce) { [style*="igsa-dot-pulse"] { animation: none !important; } }'));
}
Object.assign(__ds_scope, { StatusDot });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/StatusDot.jsx", error: String((e && e.message) || e) }); }

// components/display/Tabs.jsx
try { (() => {
function Tabs({
  items = [],
  active,
  onChange,
  style
}) {
  const [internal, setInternal] = React.useState(items[0]);
  const current = active !== undefined ? active : internal;
  const set = it => {
    if (onChange) onChange(it);
    if (active === undefined) setInternal(it);
  };
  return /*#__PURE__*/React.createElement("div", {
    role: "tablist",
    style: {
      display: 'flex',
      gap: 4,
      borderBottom: '1px solid var(--border-soft)',
      fontFamily: 'var(--font-sans)',
      ...style
    }
  }, items.map(it => {
    const sel = it === current;
    return /*#__PURE__*/React.createElement(TabBtn, {
      key: it,
      sel: sel,
      onClick: () => set(it)
    }, it);
  }));
}
function TabBtn({
  sel,
  onClick,
  children
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    role: "tab",
    "aria-selected": sel,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      appearance: 'none',
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-sans)',
      fontSize: 14,
      fontWeight: sel ? 600 : 400,
      color: sel ? 'var(--wine-600)' : hover ? 'var(--text-strong)' : 'var(--text-muted)',
      padding: '10px 14px',
      marginBottom: -1,
      borderBottom: '2px solid ' + (sel ? 'var(--wine-600)' : 'transparent'),
      transition: 'color var(--dur-fast) var(--ease-standard)'
    }
  }, children);
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Tabs.jsx", error: String((e && e.message) || e) }); }

// components/display/Tag.jsx
try { (() => {
function Tag({
  children,
  style
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      fontFamily: 'var(--font-sans)',
      fontSize: 11,
      fontWeight: 600,
      letterSpacing: 'var(--ls-wider)',
      textTransform: 'uppercase',
      color: 'var(--text-category)',
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Tag.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Toast.jsx
try { (() => {
const toastTones = {
  success: {
    border: 'var(--green-500)',
    icon: 'var(--green-500)'
  },
  warning: {
    border: 'var(--gold-400)',
    icon: 'var(--gold-500)'
  },
  danger: {
    border: 'var(--wine-500)',
    icon: 'var(--wine-600)'
  },
  info: {
    border: 'var(--sand-400)',
    icon: 'var(--ink-500)'
  }
};
function Toast({
  tone = 'info',
  title,
  children,
  onClose,
  style
}) {
  const t = toastTones[tone] || toastTones.info;
  return /*#__PURE__*/React.createElement("div", {
    role: "status",
    style: {
      display: 'flex',
      gap: 12,
      alignItems: 'flex-start',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-soft)',
      borderTop: '3px solid ' + t.border,
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-lg)',
      padding: '12px 14px',
      maxWidth: 380,
      fontFamily: 'var(--font-sans)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: t.icon,
      marginTop: 1,
      flex: 'none'
    }
  }, tone === 'success' ? /*#__PURE__*/React.createElement("svg", {
    width: "17",
    height: "17",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M22 11.08V12a10 10 0 1 1-5.93-9.14"
  }), /*#__PURE__*/React.createElement("polyline", {
    points: "22 4 12 14.01 9 11.01"
  })) : tone === 'danger' || tone === 'warning' ? /*#__PURE__*/React.createElement("svg", {
    width: "17",
    height: "17",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "12",
    y1: "9",
    x2: "12",
    y2: "13"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "12",
    y1: "17",
    x2: "12.01",
    y2: "17"
  })) : /*#__PURE__*/React.createElement("svg", {
    width: "17",
    height: "17",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "10"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "12",
    y1: "16",
    x2: "12",
    y2: "12"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "12",
    y1: "8",
    x2: "12.01",
    y2: "8"
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, title ? /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 14,
      fontWeight: 600,
      color: 'var(--text-strong)',
      marginBottom: 2
    }
  }, title) : null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      color: 'var(--text-body)',
      lineHeight: 1.5
    }
  }, children)), onClose ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onClose,
    "aria-label": "Fechar",
    style: {
      appearance: 'none',
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      color: 'var(--ink-400)',
      padding: 2,
      lineHeight: 0
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "18",
    y1: "6",
    x2: "6",
    y2: "18"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "6",
    y1: "6",
    x2: "18",
    y2: "18"
  }))) : null);
}
Object.assign(__ds_scope, { Toast });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Toast.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Input({
  label,
  hint,
  error,
  mono = false,
  style,
  inputStyle,
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 6,
      fontFamily: 'var(--font-sans)',
      ...style
    }
  }, label ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-sm)',
      fontWeight: 500,
      color: 'var(--text-strong)'
    }
  }, label) : null, /*#__PURE__*/React.createElement("input", _extends({
    style: {
      fontFamily: mono ? 'var(--font-mono)' : 'var(--font-sans)',
      fontSize: 'var(--fs-sm)',
      color: 'var(--text-strong)',
      background: 'var(--surface-card)',
      border: '1px solid ' + (error ? 'var(--wine-500)' : 'var(--border-soft)'),
      borderRadius: 'var(--radius-sm)',
      padding: '10px 12px',
      outline: 'none',
      boxShadow: focus ? 'var(--ring)' : 'none',
      transition: 'box-shadow var(--dur-fast) var(--ease-standard), border-color var(--dur-fast) var(--ease-standard)',
      ...inputStyle
    },
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false)
  }, rest)), error ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-xs)',
      color: 'var(--wine-600)'
    }
  }, error) : hint ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-xs)',
      color: 'var(--text-muted)'
    }
  }, hint) : null);
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Select({
  label,
  options = [],
  hint,
  style,
  selectStyle,
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 6,
      fontFamily: 'var(--font-sans)',
      ...style
    }
  }, label ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-sm)',
      fontWeight: 500,
      color: 'var(--text-strong)'
    }
  }, label) : null, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      display: 'flex'
    }
  }, /*#__PURE__*/React.createElement("select", _extends({
    style: {
      appearance: 'none',
      WebkitAppearance: 'none',
      width: '100%',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-sm)',
      color: 'var(--text-strong)',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-soft)',
      borderRadius: 'var(--radius-sm)',
      padding: '10px 34px 10px 12px',
      outline: 'none',
      cursor: 'pointer',
      boxShadow: focus ? 'var(--ring)' : 'none',
      transition: 'box-shadow var(--dur-fast) var(--ease-standard)',
      ...selectStyle
    },
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false)
  }, rest), options.map(o => {
    const opt = typeof o === 'string' ? {
      value: o,
      label: o
    } : o;
    return /*#__PURE__*/React.createElement("option", {
      key: opt.value,
      value: opt.value
    }, opt.label);
  })), /*#__PURE__*/React.createElement("svg", {
    style: {
      position: 'absolute',
      right: 12,
      top: '50%',
      transform: 'translateY(-50%)',
      pointerEvents: 'none',
      color: 'var(--ink-500)'
    },
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("polyline", {
    points: "6 9 12 15 18 9"
  }))), hint ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--fs-xs)',
      color: 'var(--text-muted)'
    }
  }, hint) : null);
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/CorrespondentesPanel.jsx
try { (() => {
/* ============================================================
   Painel de Correspondentes — aba "Correspondentes"
   Diretório de advogados correspondentes (cards da marca).
   ============================================================ */
const {
  Card,
  Tag: CorrTag
} = window.ImaculadaGordianoDesignSystem_59e5d5;
const corrIcons = {
  user: /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "7",
    r: "4"
  })),
  pin: /*#__PURE__*/React.createElement("svg", {
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "10",
    r: "3"
  })),
  scale: /*#__PURE__*/React.createElement("svg", {
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M12 3v18"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M6 7h12"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m3 11 3-4 3 4a3 3 0 0 1-6 0Z"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m15 11 3-4 3 4a3 3 0 0 1-6 0Z"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M7 21h10"
  }))
};
const correspondentes = [{
  nome: 'Marcos Vinícius Alves',
  oab: 'OAB/CE 18.432',
  cidade: 'Fortaleza',
  uf: 'CE',
  areas: ['Trabalhista', 'Cível'],
  audiencias: 34,
  avaliacao: '4,9',
  status: 'active'
}, {
  nome: 'Beatriz Nogueira',
  oab: 'OAB/SP 245.118',
  cidade: 'São Paulo',
  uf: 'SP',
  areas: ['Cível', 'Família'],
  audiencias: 28,
  avaliacao: '4,8',
  status: 'active'
}, {
  nome: 'Rafael Teixeira',
  oab: 'OAB/CE 21.907',
  cidade: 'Fortaleza',
  uf: 'CE',
  areas: ['Trabalhista'],
  audiencias: 41,
  avaliacao: '4,7',
  status: 'active'
}, {
  nome: 'Helena Castro',
  oab: 'OAB/SP 198.440',
  cidade: 'Guarulhos',
  uf: 'SP',
  areas: ['Previdenciário', 'Federal'],
  audiencias: 19,
  avaliacao: '4,9',
  status: 'active'
}, {
  nome: 'Tiago Moraes',
  oab: 'OAB/SP 312.005',
  cidade: 'São Paulo',
  uf: 'SP',
  areas: ['Cível', 'Empresarial'],
  audiencias: 23,
  avaliacao: '4,6',
  status: 'active'
}, {
  nome: 'Luciana Prado',
  oab: 'OAB/MG 142.770',
  cidade: 'Belo Horizonte',
  uf: 'MG',
  areas: ['Trabalhista', 'Cível'],
  audiencias: 0,
  avaliacao: '—',
  status: 'idle'
}];
function AreaChip({
  children
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-block',
      background: 'var(--sand-100)',
      color: 'var(--text-body)',
      border: '1px solid var(--border-soft)',
      fontFamily: 'var(--font-sans)',
      fontSize: 11,
      fontWeight: 500,
      padding: '2px 8px',
      borderRadius: 'var(--radius-pill)'
    }
  }, children);
}
function CorrespondenteCard({
  c
}) {
  return /*#__PURE__*/React.createElement(Card, {
    kicker: 'Correspondente · ' + c.uf,
    title: c.nome,
    status: c.status,
    icon: corrIcons.user,
    hoverable: true,
    footer: /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontFamily: 'var(--font-sans)',
        fontSize: 12,
        color: 'var(--text-muted)'
      }
    }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("strong", {
      style: {
        fontFamily: 'var(--font-mono)',
        fontWeight: 600,
        color: 'var(--text-strong)'
      }
    }, c.audiencias), " audi\xEAncias realizadas"), /*#__PURE__*/React.createElement("span", null, "Avalia\xE7\xE3o ", /*#__PURE__*/React.createElement("strong", {
      style: {
        fontFamily: 'var(--font-mono)',
        fontWeight: 600,
        color: c.avaliacao === '—' ? 'var(--text-faint)' : 'var(--gold-600)'
      }
    }, c.avaliacao)))
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12,
      color: 'var(--text-strong)'
    }
  }, c.oab), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      fontFamily: 'var(--font-sans)',
      fontSize: 12.5,
      color: 'var(--text-body)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--wine-600)',
      display: 'flex'
    }
  }, corrIcons.pin), c.cidade, " \xB7 ", c.uf), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--rose-400)',
      display: 'flex',
      marginRight: 2
    }
  }, corrIcons.scale), c.areas.map(a => /*#__PURE__*/React.createElement(AreaChip, {
    key: a
  }, a)))));
}
function CorrespondentesPanel() {
  return /*#__PURE__*/React.createElement("section", null, /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement(CorrTag, null, "Rede \xB7 Correspondentes"), /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: '8px 0 2px',
      fontFamily: 'var(--font-serif)',
      fontSize: 'var(--fs-2xl)',
      fontWeight: 600,
      color: 'var(--text-strong)'
    }
  }, "Diret\xF3rio de correspondentes"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-sm)',
      color: 'var(--text-muted)'
    }
  }, "Advogados credenciados para dilig\xEAncias e audi\xEAncias em todo o territ\xF3rio nacional.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
      gap: 20,
      alignItems: 'start'
    }
  }, correspondentes.map(c => /*#__PURE__*/React.createElement(CorrespondenteCard, {
    key: c.oab,
    c: c
  }))));
}
window.CorrespondentesPanel = CorrespondentesPanel;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/CorrespondentesPanel.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/FinanceiroPanel.jsx
try { (() => {
/* ============================================================
   Painel de Correspondentes — aba "Gestão Financeira"
   Indicadores de regras de pagamento, importação de planilha,
   filtros e tabela de lançamentos (Número CNJ em IBM Plex Mono).
   ============================================================ */
const {
  Button,
  Input,
  Select,
  Badge,
  StatusDot,
  Tag
} = window.ImaculadaGordianoDesignSystem_59e5d5;

/* ---- formatação brasileira ---- */
const brl = n => n.toLocaleString('pt-BR', {
  style: 'currency',
  currency: 'BRL'
});
const numBR = n => n.toLocaleString('pt-BR');

/* ---- ícones Lucide (stroke 1.5) ---- */
const finIcons = {
  upload: /*#__PURE__*/React.createElement("svg", {
    width: "26",
    height: "26",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 14.9A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 2.5 8.2"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M12 12v9"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m16 16-4-4-4 4"
  })),
  sheet: /*#__PURE__*/React.createElement("svg", {
    width: "18",
    height: "18",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M14 2v5h5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 13h8"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 17h8"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10 9h1"
  })),
  check: /*#__PURE__*/React.createElement("svg", {
    width: "16",
    height: "16",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M21.8 10A10 10 0 1 1 12 2"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m9 11 3 3L22 4"
  })),
  award: /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "8",
    r: "6"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M15.5 13.6 17 22l-5-3-5 3 1.5-8.4"
  })),
  target: /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "10"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "2"
  })),
  filter: /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M3 4.5h18l-7 8v6l-4 2v-8z"
  })),
  download: /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M7 10l5 5 5-5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M12 15V3"
  }))
};

/* ============================================================
   Regras de pagamento (flexíveis: contagem, município, valor)
   ============================================================ */
const regras = [{
  cliente: 'IMC Saste Construções, Serviços e Comércio Ltda.',
  criterio: 'Quantidade superior a 30 audiências realizadas',
  parametro: 'Audiências realizadas no período',
  atual: 34,
  meta: 30,
  tipo: 'count',
  unidade: 'audiências'
}, {
  cliente: 'Banco Meridional S.A.',
  criterio: 'Meta trimestral de comparecimentos',
  parametro: 'Audiências realizadas no trimestre',
  atual: 58,
  meta: 50,
  tipo: 'count',
  unidade: 'audiências'
}, {
  cliente: 'Transportadora Vale Verde Ltda.',
  criterio: 'Concentração por município',
  parametro: 'Audiências no município de São Paulo/SP',
  atual: 14,
  meta: 20,
  tipo: 'count',
  unidade: 'audiências'
}, {
  cliente: 'Construtora Horizonte S.A.',
  criterio: 'Valor acumulado em correspondências',
  parametro: 'Valor pago a correspondentes no mês',
  atual: 21450,
  meta: 25000,
  tipo: 'currency',
  unidade: ''
}];
function ProgressBar({
  pct,
  reached
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      height: 7,
      borderRadius: 'var(--radius-pill)',
      background: 'var(--sand-200)',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: Math.min(100, pct) + '%',
      height: '100%',
      borderRadius: 'var(--radius-pill)',
      background: reached ? 'var(--green-500)' : 'var(--wine-600)',
      transition: 'width var(--dur-slow) var(--ease-out)'
    }
  }));
}
function IndicatorCard({
  regra
}) {
  const fmt = regra.tipo === 'currency' ? brl : numBR;
  const reached = regra.atual >= regra.meta;
  const pct = Math.round(regra.atual / regra.meta * 100);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      background: reached ? 'linear-gradient(180deg, var(--gold-50), var(--white) 46%)' : 'var(--white)',
      border: reached ? '1.5px solid var(--gold-400)' : 'var(--card-border)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: reached ? 'var(--shadow-md)' : 'var(--card-shadow)',
      padding: '18px 20px 20px',
      display: 'flex',
      flexDirection: 'column',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 16,
      right: 16
    }
  }, /*#__PURE__*/React.createElement(StatusDot, {
    tone: reached ? 'active' : 'idle',
    pulse: reached
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      paddingRight: 18
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: reached ? 'var(--gold-600)' : 'var(--wine-600)',
      display: 'flex'
    }
  }, finIcons.target), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 13.5,
      fontWeight: 600,
      color: 'var(--text-strong)',
      lineHeight: 1.25
    }
  }, regra.cliente)), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12,
      color: 'var(--text-muted)',
      marginBottom: 2
    }
  }, regra.criterio), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 11.5,
      color: 'var(--text-faint)'
    }
  }, regra.parametro)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 26,
      fontWeight: 600,
      color: reached ? 'var(--green-700)' : 'var(--text-strong)',
      letterSpacing: '-0.01em'
    }
  }, fmt(regra.atual)), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12.5,
      color: 'var(--text-muted)'
    }
  }, "/ meta ", fmt(regra.meta), regra.unidade ? ' ' + regra.unidade : '')), /*#__PURE__*/React.createElement(ProgressBar, {
    pct: pct,
    reached: reached
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 11.5,
      color: reached ? 'var(--green-700)' : 'var(--text-muted)'
    }
  }, pct, "% da meta"), reached ? /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      background: 'var(--green-100)',
      color: 'var(--green-700)',
      border: '1px solid color-mix(in srgb, var(--green-500) 35%, transparent)',
      fontFamily: 'var(--font-sans)',
      fontSize: 11.5,
      fontWeight: 600,
      padding: '4px 10px',
      borderRadius: 'var(--radius-pill)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex'
    }
  }, finIcons.award), "Regra atingida") : /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 11.5,
      fontWeight: 500,
      color: 'var(--gold-600)'
    }
  }, "Em andamento")));
}

/* ============================================================
   Importar planilha (.xlsx / .csv) com estados de upload
   ============================================================ */
function ImportZone() {
  const inputRef = React.useRef(null);
  const [state, setState] = React.useState('idle'); // idle | uploading | done
  const [fileName, setFileName] = React.useState('');
  const [pct, setPct] = React.useState(0);
  const [registros, setRegistros] = React.useState(0);
  const pick = () => inputRef.current && inputRef.current.click();
  const onFile = e => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    setFileName(f.name);
    setState('uploading');
    setPct(0);
    let p = 0;
    window.clearInterval(window.__igsaUpT);
    window.__igsaUpT = window.setInterval(() => {
      p += Math.random() * 16 + 8;
      if (p >= 100) {
        p = 100;
        window.clearInterval(window.__igsaUpT);
        setPct(100);
        setRegistros(128);
        window.setTimeout(() => setState('done'), 320);
      } else {
        setPct(Math.round(p));
      }
    }, 180);
    e.target.value = '';
  };
  const reset = () => {
    setState('idle');
    setFileName('');
    setPct(0);
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--white)',
      border: '1.5px dashed var(--border-strong)',
      borderRadius: 'var(--radius-lg)',
      padding: '22px 24px',
      display: 'flex',
      alignItems: 'center',
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("input", {
    ref: inputRef,
    type: "file",
    accept: ".xlsx,.xls,.csv",
    onChange: onFile,
    style: {
      display: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 56,
      height: 56,
      flexShrink: 0,
      borderRadius: 'var(--radius-md)',
      background: 'var(--rose-soft)',
      color: 'var(--rose-400)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, finIcons.upload), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, state === 'idle' ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 14.5,
      fontWeight: 600,
      color: 'var(--text-strong)'
    }
  }, "Importar planilha de audi\xEAncias"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12.5,
      color: 'var(--text-muted)',
      marginTop: 2
    }
  }, "Carregamento em massa \u2014 arquivos ", /*#__PURE__*/React.createElement("strong", {
    style: {
      fontWeight: 600,
      color: 'var(--text-body)'
    }
  }, ".xlsx"), " ou ", /*#__PURE__*/React.createElement("strong", {
    style: {
      fontWeight: 600,
      color: 'var(--text-body)'
    }
  }, ".csv"), ". A primeira linha deve conter os cabe\xE7alhos das colunas.")) : null, state === 'uploading' ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 12,
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 8,
      fontFamily: 'var(--font-sans)',
      fontSize: 13.5,
      fontWeight: 600,
      color: 'var(--text-strong)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--wine-600)',
      display: 'flex'
    }
  }, finIcons.sheet), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12.5
    }
  }, fileName)), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12.5,
      color: 'var(--wine-600)',
      fontWeight: 600
    }
  }, pct, "%")), /*#__PURE__*/React.createElement(ProgressBar, {
    pct: pct,
    reached: false
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12,
      color: 'var(--text-muted)',
      marginTop: 6
    }
  }, "Enviando e validando registros\u2026")) : null, state === 'done' ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--green-500)',
      display: 'flex'
    }
  }, finIcons.check), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 14,
      fontWeight: 600,
      color: 'var(--text-strong)'
    }
  }, "Importa\xE7\xE3o conclu\xEDda com sucesso."), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12.5,
      color: 'var(--text-muted)',
      marginTop: 2
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)'
    }
  }, fileName), " \xB7 ", numBR(registros), " registros processados."))) : null), /*#__PURE__*/React.createElement("div", {
    style: {
      flexShrink: 0
    }
  }, state === 'done' ? /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "sm",
    onClick: reset
  }, "Importar outra") : /*#__PURE__*/React.createElement(Button, {
    variant: "accent",
    size: "sm",
    icon: finIcons.upload,
    onClick: pick,
    disabled: state === 'uploading'
  }, "Importar planilha")));
}

/* ============================================================
   Lançamentos — tabela completa
   ============================================================ */
const lancamentos = [{
  data: '09/06/2026',
  hora: '14h30',
  id: 'AUD-2026-0412',
  natureza: 'Trabalhista',
  cnj: '0007821-09.2024.8.06.0001',
  tipo: 'Instrução / Testemunhal',
  descricao: 'Audiência de instrução e julgamento',
  responsavel: 'Dr. Marcos Vinícius Alves',
  valor: 320.00,
  cliente: 'IMC Saste Construções, Serviços e Comércio Ltda.',
  contraria: 'João Batista dos Santos',
  modalidade: 'Presencial',
  solicitacao: 'Comparecimento e relatório',
  local: '12ª Vara do Trabalho',
  cidade: 'Fortaleza',
  uf: 'CE',
  preposto: 'Ana Lúcia Ferreira',
  corresp: 'Dr. Marcos V. Alves · OAB/CE 18.432',
  classificacao: 'Estratégico',
  obs: 'Levar quesitos da reclamada.',
  empresa: 'Correspondência Jurídica Nordeste Ltda.',
  arquivo: 'audiencias_jun2026.xlsx'
}, {
  data: '09/06/2026',
  hora: '09h00',
  id: 'AUD-2026-0413',
  natureza: 'Cível',
  cnj: '0001234-56.2025.8.26.0100',
  tipo: 'Conciliação / CEJUSC',
  descricao: 'Tentativa de acordo — fase inicial',
  responsavel: 'Dra. Beatriz Nogueira',
  valor: 280.00,
  cliente: 'Transportadora Vale Verde Ltda.',
  contraria: 'Comercial Atlântico Ltda.',
  modalidade: 'Virtual',
  solicitacao: 'Comparecimento com proposta',
  local: '3ª Vara Cível',
  cidade: 'São Paulo',
  uf: 'SP',
  preposto: 'Carlos Eduardo Lima',
  corresp: 'Dra. B. Nogueira · OAB/SP 245.118',
  classificacao: 'Padrão',
  obs: 'Alçada de acordo até R$ 15.000,00.',
  empresa: 'Rede Forense Brasil ME',
  arquivo: 'audiencias_jun2026.xlsx'
}, {
  data: '10/06/2026',
  hora: '11h15',
  id: 'AUD-2026-0418',
  natureza: 'Trabalhista',
  cnj: '0009912-33.2025.8.06.0112',
  tipo: 'Una / Inicial',
  descricao: 'Audiência una',
  responsavel: 'Dr. Rafael Teixeira',
  valor: 350.00,
  cliente: 'IMC Saste Construções, Serviços e Comércio Ltda.',
  contraria: 'Sindicato dos Trabalhadores',
  modalidade: 'Presencial',
  solicitacao: 'Comparecimento e preposto',
  local: '5ª Vara do Trabalho',
  cidade: 'Fortaleza',
  uf: 'CE',
  preposto: 'Ana Lúcia Ferreira',
  corresp: 'Dr. R. Teixeira · OAB/CE 21.907',
  classificacao: 'Estratégico',
  obs: '—',
  empresa: 'Correspondência Jurídica Nordeste Ltda.',
  arquivo: 'audiencias_jun2026.xlsx'
}, {
  data: '11/06/2026',
  hora: '15h45',
  id: 'AUD-2026-0421',
  natureza: 'Previdenciário',
  cnj: '0003310-77.2025.8.26.0224',
  tipo: 'Justificação / Perícia',
  descricao: 'Audiência de justificação',
  responsavel: 'Dra. Helena Castro',
  valor: 410.00,
  cliente: 'Banco Meridional S.A.',
  contraria: 'Espólio de Raimundo Alves',
  modalidade: 'Híbrida',
  solicitacao: 'Acompanhamento de perícia',
  local: '2ª Vara Federal',
  cidade: 'Guarulhos',
  uf: 'SP',
  preposto: 'Mariana Duarte',
  corresp: 'Dra. H. Castro · OAB/SP 198.440',
  classificacao: 'Sensível',
  obs: 'Confirmar laudo prévio.',
  empresa: 'JurisApoio Correspondentes Ltda.',
  arquivo: 'audiencias_jun2026.xlsx'
}, {
  data: '12/06/2026',
  hora: '08h30',
  id: 'AUD-2026-0427',
  natureza: 'Cível',
  cnj: '0002207-18.2024.8.26.0011',
  tipo: 'Instrução / Documental',
  descricao: 'Oitiva de testemunhas',
  responsavel: 'Dr. Tiago Moraes',
  valor: 300.00,
  cliente: 'Construtora Horizonte S.A.',
  contraria: 'Condomínio Edifício Aurora',
  modalidade: 'Presencial',
  solicitacao: 'Comparecimento e relatório',
  local: '11ª Vara Cível',
  cidade: 'São Paulo',
  uf: 'SP',
  preposto: 'Roberto Salles',
  corresp: 'Dr. T. Moraes · OAB/SP 312.005',
  classificacao: 'Padrão',
  obs: 'Rol de 3 testemunhas.',
  empresa: 'Rede Forense Brasil ME',
  arquivo: 'audiencias_jun2026.xlsx'
}, {
  data: '12/06/2026',
  hora: '13h00',
  id: 'AUD-2026-0431',
  natureza: 'Família',
  cnj: '0004415-90.2025.8.26.0224',
  tipo: 'Conciliação / Inicial',
  descricao: 'Audiência de conciliação',
  responsavel: 'Dra. Beatriz Nogueira',
  valor: 260.00,
  cliente: 'Transportadora Vale Verde Ltda.',
  contraria: 'Particular — sigiloso',
  modalidade: 'Virtual',
  solicitacao: 'Comparecimento',
  local: '1ª Vara de Família',
  cidade: 'Campinas',
  uf: 'SP',
  preposto: '—',
  corresp: 'Dra. B. Nogueira · OAB/SP 245.118',
  classificacao: 'Padrão',
  obs: 'Segredo de justiça.',
  empresa: 'JurisApoio Correspondentes Ltda.',
  arquivo: 'audiencias_jun2026.xlsx'
}, {
  data: '13/06/2026',
  hora: '10h00',
  id: 'AUD-2026-0440',
  natureza: 'Trabalhista',
  cnj: '0005528-44.2025.8.06.0001',
  tipo: 'Instrução / Testemunhal',
  descricao: 'Audiência de instrução',
  responsavel: 'Dr. Rafael Teixeira',
  valor: 350.00,
  cliente: 'IMC Saste Construções, Serviços e Comércio Ltda.',
  contraria: 'Pedro Henrique Souza',
  modalidade: 'Presencial',
  solicitacao: 'Comparecimento e preposto',
  local: '8ª Vara do Trabalho',
  cidade: 'Fortaleza',
  uf: 'CE',
  preposto: 'Ana Lúcia Ferreira',
  corresp: 'Dr. R. Teixeira · OAB/CE 21.907',
  classificacao: 'Estratégico',
  obs: '—',
  empresa: 'Correspondência Jurídica Nordeste Ltda.',
  arquivo: 'audiencias_jun2026.xlsx'
}, {
  data: '13/06/2026',
  hora: '16h20',
  id: 'AUD-2026-0444',
  natureza: 'Cível',
  cnj: '0006640-12.2025.8.26.0100',
  tipo: 'Conciliação / CEJUSC',
  descricao: 'Sessão de mediação',
  responsavel: 'Dr. Tiago Moraes',
  valor: 290.00,
  cliente: 'Banco Meridional S.A.',
  contraria: 'Lojas Brasil Central Ltda.',
  modalidade: 'Virtual',
  solicitacao: 'Comparecimento com proposta',
  local: 'CEJUSC Central',
  cidade: 'São Paulo',
  uf: 'SP',
  preposto: 'Mariana Duarte',
  corresp: 'Dr. T. Moraes · OAB/SP 312.005',
  classificacao: 'Padrão',
  obs: 'Proposta inicial enviada.',
  empresa: 'Rede Forense Brasil ME',
  arquivo: 'audiencias_jun2026.xlsx'
}];
const COLS = [{
  k: 'data',
  label: 'Data',
  mono: true,
  w: 96
}, {
  k: 'hora',
  label: 'Hora de Início',
  mono: true,
  w: 110
}, {
  k: 'id',
  label: 'ID',
  mono: true,
  w: 122
}, {
  k: 'natureza',
  label: 'Natureza',
  w: 118
}, {
  k: 'cnj',
  label: 'Número CNJ',
  mono: true,
  w: 196
}, {
  k: 'tipo',
  label: 'Tipo / Subtipo',
  w: 168
}, {
  k: 'descricao',
  label: 'Descrição',
  w: 230
}, {
  k: 'responsavel',
  label: 'Responsável pela Audiência',
  w: 190
}, {
  k: 'valor',
  label: 'Valor',
  mono: true,
  align: 'right',
  w: 110,
  money: true
}, {
  k: 'cliente',
  label: 'Cliente',
  w: 250,
  strong: true
}, {
  k: 'contraria',
  label: 'Parte Contrária',
  w: 190
}, {
  k: 'modalidade',
  label: 'Modalidade',
  w: 116,
  chip: true
}, {
  k: 'solicitacao',
  label: 'Solicitação',
  w: 200
}, {
  k: 'local',
  label: 'Local',
  w: 160
}, {
  k: 'cidade',
  label: 'Cidade',
  w: 120
}, {
  k: 'uf',
  label: 'UF',
  mono: true,
  align: 'center',
  w: 54
}, {
  k: 'preposto',
  label: 'Preposto',
  w: 160
}, {
  k: 'corresp',
  label: 'Dados dos Correspondentes',
  w: 230,
  mono: true
}, {
  k: 'classificacao',
  label: 'Classificação do Processo',
  w: 170
}, {
  k: 'obs',
  label: 'Observações',
  w: 220
}, {
  k: 'empresa',
  label: 'Empresa Contratada',
  w: 240
}, {
  k: 'arquivo',
  label: 'Arquivo de Origem',
  w: 190,
  mono: true
}];
const chipTone = {
  Presencial: {
    bg: 'var(--wine-50)',
    fg: 'var(--wine-700)',
    bd: 'var(--rose-300)'
  },
  Virtual: {
    bg: 'var(--gold-50)',
    fg: 'var(--gold-600)',
    bd: 'var(--gold-200)'
  },
  Híbrida: {
    bg: 'var(--green-100)',
    fg: 'var(--green-700)',
    bd: 'color-mix(in srgb, var(--green-500) 30%, transparent)'
  }
};
function Chip({
  value
}) {
  const t = chipTone[value] || {
    bg: 'var(--sand-200)',
    fg: 'var(--text-body)',
    bd: 'var(--border-strong)'
  };
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-block',
      background: t.bg,
      color: t.fg,
      border: '1px solid ' + t.bd,
      fontFamily: 'var(--font-sans)',
      fontSize: 11.5,
      fontWeight: 500,
      padding: '2px 9px',
      borderRadius: 'var(--radius-pill)',
      whiteSpace: 'nowrap'
    }
  }, value);
}
function TableRow({
  row
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("tr", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      background: hover ? 'var(--sand-50)' : 'var(--white)',
      transition: 'background var(--dur-fast) var(--ease-standard)'
    }
  }, COLS.map(c => /*#__PURE__*/React.createElement("td", {
    key: c.k,
    style: {
      padding: '11px 14px',
      borderBottom: '1px solid var(--border-soft)',
      fontFamily: c.mono ? 'var(--font-mono)' : 'var(--font-sans)',
      fontSize: c.mono ? 12 : 12.5,
      fontWeight: c.strong ? 600 : c.money ? 500 : 400,
      color: c.strong || c.money ? 'var(--text-strong)' : 'var(--text-body)',
      textAlign: c.align || 'left',
      whiteSpace: c.k === 'cliente' || c.k === 'empresa' || c.k === 'descricao' || c.k === 'obs' || c.k === 'solicitacao' ? 'normal' : 'nowrap',
      verticalAlign: 'top',
      lineHeight: 1.4
    }
  }, c.money ? brl(row.valor) : c.chip ? /*#__PURE__*/React.createElement(Chip, {
    value: row[c.k]
  }) : row[c.k])));
}
function FinanceiroPanel() {
  const [fCliente, setFCliente] = React.useState('Todos os clientes');
  const [fModal, setFModal] = React.useState('Todas as modalidades');
  const [fEmpresa, setFEmpresa] = React.useState('Todas as empresas');
  const [fData, setFData] = React.useState('');
  const clientes = ['Todos os clientes', ...Array.from(new Set(lancamentos.map(l => l.cliente)))];
  const empresas = ['Todas as empresas', ...Array.from(new Set(lancamentos.map(l => l.empresa)))];
  const modalidades = ['Todas as modalidades', 'Presencial', 'Virtual', 'Híbrida'];
  const toIso = d => {
    const [dd, mm, yy] = d.split('/');
    return yy + '-' + mm + '-' + dd;
  };
  const rows = lancamentos.filter(l => (fCliente === 'Todos os clientes' || l.cliente === fCliente) && (fModal === 'Todas as modalidades' || l.modalidade === fModal) && (fEmpresa === 'Todas as empresas' || l.empresa === fEmpresa) && (!fData || toIso(l.data) === fData));
  const total = rows.reduce((s, r) => s + r.valor, 0);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 28
    }
  }, /*#__PURE__*/React.createElement("section", null, /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement(Tag, null, "Indicadores \xB7 Regras de Pagamento"), /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: '8px 0 2px',
      fontFamily: 'var(--font-serif)',
      fontSize: 'var(--fs-2xl)',
      fontWeight: 600,
      color: 'var(--text-strong)'
    }
  }, "Regras de pagamento por cliente"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-sm)',
      color: 'var(--text-muted)'
    }
  }, "Par\xE2metros configur\xE1veis \u2014 contagem de audi\xEAncias, concentra\xE7\xE3o por munic\xEDpio ou valores acumulados. Clientes eleg\xEDveis recebem o selo ", /*#__PURE__*/React.createElement("strong", {
    style: {
      fontWeight: 600,
      color: 'var(--green-700)'
    }
  }, "Regra atingida"), ".")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(290px, 1fr))',
      gap: 18
    }
  }, regras.map(r => /*#__PURE__*/React.createElement(IndicatorCard, {
    key: r.cliente,
    regra: r
  })))), /*#__PURE__*/React.createElement(ImportZone, null), /*#__PURE__*/React.createElement("section", {
    style: {
      background: 'var(--white)',
      border: 'var(--card-border)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--card-shadow)',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      justifyContent: 'space-between',
      gap: 16,
      padding: '20px 22px 14px'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Tag, null, "Lan\xE7amentos \xB7 Audi\xEAncias"), /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: '6px 0 0',
      fontFamily: 'var(--font-serif)',
      fontSize: 'var(--fs-xl)',
      fontWeight: 600,
      color: 'var(--text-strong)'
    }
  }, "Gest\xE3o financeira de audi\xEAncias")), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "sm",
    icon: finIcons.download
  }, "Exportar")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      flexWrap: 'wrap',
      padding: '0 22px 16px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      color: 'var(--text-muted)',
      fontFamily: 'var(--font-sans)',
      fontSize: 12.5,
      fontWeight: 500,
      marginRight: 4
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex'
    }
  }, finIcons.filter), "Filtrar"), /*#__PURE__*/React.createElement(Input, {
    type: "date",
    value: fData,
    onChange: e => setFData(e.target.value),
    style: {
      minWidth: 0
    },
    inputStyle: {
      width: 150
    }
  }), /*#__PURE__*/React.createElement(Select, {
    options: clientes,
    value: fCliente,
    onChange: e => setFCliente(e.target.value),
    selectStyle: {
      minWidth: 200
    }
  }), /*#__PURE__*/React.createElement(Select, {
    options: modalidades,
    value: fModal,
    onChange: e => setFModal(e.target.value),
    selectStyle: {
      minWidth: 170
    }
  }), /*#__PURE__*/React.createElement(Select, {
    options: empresas,
    value: fEmpresa,
    onChange: e => setFEmpresa(e.target.value),
    selectStyle: {
      minWidth: 210
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      overflowX: 'auto'
    }
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      borderCollapse: 'collapse',
      width: '100%',
      minWidth: 3200
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, COLS.map(c => /*#__PURE__*/React.createElement("th", {
    key: c.k,
    style: {
      position: 'sticky',
      top: 0,
      zIndex: 1,
      background: 'var(--sand-100)',
      color: 'var(--text-muted)',
      fontFamily: 'var(--font-sans)',
      fontSize: 10.5,
      fontWeight: 700,
      letterSpacing: '0.06em',
      textTransform: 'uppercase',
      textAlign: c.align || 'left',
      padding: '11px 14px',
      borderBottom: '1px solid var(--border-strong)',
      whiteSpace: 'nowrap',
      minWidth: c.w,
      width: c.w
    }
  }, c.label)))), /*#__PURE__*/React.createElement("tbody", null, rows.map(r => /*#__PURE__*/React.createElement(TableRow, {
    key: r.id,
    row: r
  }))))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 12,
      padding: '14px 22px',
      borderTop: '1px solid var(--border-soft)',
      background: 'var(--sand-50)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12.5,
      color: 'var(--text-muted)'
    }
  }, rows.length, " ", rows.length === 1 ? 'lançamento' : 'lançamentos', " exibidos"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12.5,
      color: 'var(--text-muted)'
    }
  }, "Total dos lan\xE7amentos\xA0\xA0", /*#__PURE__*/React.createElement("strong", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 14,
      fontWeight: 600,
      color: 'var(--text-strong)'
    }
  }, brl(total))))));
}
window.FinanceiroPanel = FinanceiroPanel;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/FinanceiroPanel.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/Header.jsx
try { (() => {
const {
  Button,
  Avatar
} = window.ImaculadaGordianoDesignSystem_59e5d5;
function DashHeader({
  onControladoria
}) {
  const [nav, setNav] = React.useState('Painel');
  const items = ['Painel', 'Processos', 'Agenda', 'Relatórios'];
  return /*#__PURE__*/React.createElement("header", {
    style: {
      background: 'var(--gradient-wine)',
      padding: '0 32px',
      display: 'flex',
      alignItems: 'center',
      gap: 32,
      height: 76,
      boxShadow: 'var(--shadow-md)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/crest.png",
    alt: "",
    width: "40",
    height: "40",
    style: {
      borderRadius: 'var(--radius-sm)'
    }
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      color: 'var(--text-on-wine)',
      fontSize: 15,
      fontWeight: 600,
      letterSpacing: 'var(--ls-caps)',
      whiteSpace: 'nowrap'
    }
  }, "IMACULADA GORDIANO"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      color: 'var(--text-on-wine-muted)',
      fontSize: 8.5,
      letterSpacing: '0.3em'
    }
  }, "SOCIEDADE DE ADVOGADOS"))), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      gap: 4,
      flex: 1
    }
  }, items.map(it => /*#__PURE__*/React.createElement("button", {
    key: it,
    type: "button",
    onClick: () => setNav(it),
    style: {
      appearance: 'none',
      border: 'none',
      cursor: 'pointer',
      background: nav === it ? 'rgba(255,255,255,0.13)' : 'transparent',
      color: nav === it ? '#fff' : 'var(--text-on-wine-muted)',
      fontFamily: 'var(--font-sans)',
      fontSize: 13.5,
      fontWeight: nav === it ? 600 : 400,
      padding: '8px 14px',
      borderRadius: 'var(--radius-sm)',
      transition: 'background var(--dur-fast) var(--ease-standard), color var(--dur-fast) var(--ease-standard)'
    }
  }, it))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "accent",
    size: "sm",
    onClick: onControladoria
  }, "Controladoria"), /*#__PURE__*/React.createElement(Avatar, {
    name: "Imaculada Gordiano"
  })));
}
window.DashHeader = DashHeader;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/Header.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/Panels.jsx
try { (() => {
const {
  Card,
  Badge,
  Tag,
  StatusDot,
  Tabs,
  Button
} = window.ImaculadaGordianoDesignSystem_59e5d5;
const icons = {
  doc: /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
  }), /*#__PURE__*/React.createElement("polyline", {
    points: "14 2 14 8 20 8"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "16",
    y1: "13",
    x2: "8",
    y2: "13"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "16",
    y1: "17",
    x2: "8",
    y2: "17"
  })),
  clock: /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "10"
  }), /*#__PURE__*/React.createElement("polyline", {
    points: "12 6 12 12 16 14"
  })),
  gavel: /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M14 13l7.5 7.5a1.5 1.5 0 0 1-2.1 2.1L12 15.1"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M9 4l7 7"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M6 7l7 7"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "6.6",
    y: "2.6",
    width: "5",
    height: "3",
    rx: "0.8",
    transform: "rotate(45 9 4)"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "3.6",
    y: "9.6",
    width: "5",
    height: "3",
    rx: "0.8",
    transform: "rotate(45 6 11)"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M2 21h8"
  }))
};
const pubs = [{
  num: '0001234-56.2025.8.26.0100',
  org: '3ª Vara Cível · São Paulo',
  kind: 'Intimação',
  when: 'hoje, 08h02'
}, {
  num: '0007821-09.2024.8.06.0001',
  org: '12ª Vara do Trabalho · Fortaleza',
  kind: 'Despacho',
  when: 'hoje, 07h45'
}, {
  num: '0003310-77.2025.8.26.0224',
  org: '2ª Vara de Família · Guarulhos',
  kind: 'Sentença',
  when: 'ontem, 18h21'
}];
const prazos = [{
  num: '0001234-56.2025.8.26.0100',
  act: 'Contestação',
  days: 2,
  tone: 'danger'
}, {
  num: '0009912-33.2025.8.06.0112',
  act: 'Recurso ordinário',
  days: 5,
  tone: 'warning'
}, {
  num: '0002207-18.2024.8.26.0011',
  act: 'Manifestação',
  days: 11,
  tone: 'success'
}];
const audiencias = [{
  num: '0007821-09.2024.8.06.0001',
  kind: 'Instrução e julgamento',
  when: '11/06 · 14h30',
  where: '12ª Vara do Trabalho'
}, {
  num: '0003310-77.2025.8.26.0224',
  kind: 'Conciliação',
  when: '15/06 · 09h00',
  where: 'CEJUSC Guarulhos'
}];
function RowNum({
  children
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12,
      color: 'var(--text-strong)'
    }
  }, children);
}
function ListRow({
  children,
  last
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 12,
      padding: '10px 8px',
      margin: '0 -8px',
      borderBottom: last ? 'none' : '1px solid var(--border-soft)',
      background: hover ? 'var(--sand-50)' : 'transparent',
      borderRadius: 'var(--radius-sm)',
      cursor: 'pointer',
      transition: 'background var(--dur-fast) var(--ease-standard)'
    }
  }, children);
}
function PubsPanel() {
  const [tab, setTab] = React.useState('Todas');
  const shown = tab === 'Todas' ? pubs : pubs.filter(p => p.kind === tab.replace(/ões$/, 'ão'));
  return /*#__PURE__*/React.createElement(Card, {
    kicker: "Automa\xE7\xE3o \xB7 Di\xE1rio",
    title: "Painel de Publica\xE7\xF5es",
    status: "active",
    icon: icons.doc,
    footer: "Captura autom\xE1tica do Di\xE1rio Oficial \xB7 atualizado \xE0s 08h12"
  }, /*#__PURE__*/React.createElement(Tabs, {
    items: ['Todas', 'Intimações', 'Despachos'],
    active: tab === 'Despachos' ? 'Despachos' : tab,
    onChange: setTab,
    style: {
      marginBottom: 8
    }
  }), (tab === 'Despachos' ? pubs.filter(p => p.kind === 'Despacho') : shown).map((p, i, arr) => /*#__PURE__*/React.createElement(ListRow, {
    key: p.num + p.kind,
    last: i === arr.length - 1
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 2
    }
  }, /*#__PURE__*/React.createElement(RowNum, null, p.num), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)'
    }
  }, p.org)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-end',
      gap: 2
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      fontWeight: 500,
      color: 'var(--wine-600)'
    }
  }, p.kind), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11,
      color: 'var(--text-faint)'
    }
  }, p.when)))));
}
function PrazosPanel({
  onAction
}) {
  return /*#__PURE__*/React.createElement(Card, {
    kicker: "Prazos \xB7 Controle",
    title: "Prazos Preclusivos",
    status: "warning",
    icon: icons.clock,
    footer: /*#__PURE__*/React.createElement("span", null, "3 prazos nos pr\xF3ximos 15 dias")
  }, prazos.map((p, i) => /*#__PURE__*/React.createElement(ListRow, {
    key: p.num,
    last: i === prazos.length - 1
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 2
    }
  }, /*#__PURE__*/React.createElement(RowNum, null, p.num), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)'
    }
  }, p.act)), /*#__PURE__*/React.createElement(Badge, {
    tone: p.tone,
    dot: true
  }, p.days === 2 ? 'Vence em 2 dias' : 'em ' + p.days + ' dias'))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "sm",
    onClick: onAction
  }, "Registrar andamento")));
}
function AudienciasPanel() {
  return /*#__PURE__*/React.createElement(Card, {
    kicker: "Audi\xEAncias \xB7 Agenda",
    title: "Pauta de Audi\xEAncias",
    status: "active",
    icon: icons.gavel,
    footer: "Pr\xF3xima audi\xEAncia em 2 dias"
  }, audiencias.map((a, i) => /*#__PURE__*/React.createElement(ListRow, {
    key: a.num,
    last: i === audiencias.length - 1
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 2
    }
  }, /*#__PURE__*/React.createElement(RowNum, null, a.num), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)'
    }
  }, a.kind, " \xB7 ", a.where)), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12,
      color: 'var(--text-strong)',
      whiteSpace: 'nowrap'
    }
  }, a.when))));
}
Object.assign(window, {
  PubsPanel,
  PrazosPanel,
  AudienciasPanel
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/Panels.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.StatusDot = __ds_scope.StatusDot;

__ds_ns.Tabs = __ds_scope.Tabs;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.Toast = __ds_scope.Toast;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Select = __ds_scope.Select;

})();
