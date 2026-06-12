import { useState } from "react";

type ButtonType = "number" | "operator" | "equals" | "clear" | "special";

interface CalcButton {
  label: string;
  value: string;
  type: ButtonType;
  span?: number;
}

const buttons: CalcButton[] = [
  { label: "AC", value: "clear", type: "clear" },
  { label: "+/-", value: "negate", type: "special" },
  { label: "%", value: "%", type: "special" },
  { label: "÷", value: "/", type: "operator" },
  { label: "7", value: "7", type: "number" },
  { label: "8", value: "8", type: "number" },
  { label: "9", value: "9", type: "number" },
  { label: "×", value: "*", type: "operator" },
  { label: "4", value: "4", type: "number" },
  { label: "5", value: "5", type: "number" },
  { label: "6", value: "6", type: "number" },
  { label: "−", value: "-", type: "operator" },
  { label: "1", value: "1", type: "number" },
  { label: "2", value: "2", type: "number" },
  { label: "3", value: "3", type: "number" },
  { label: "+", value: "+", type: "operator" },
  { label: "0", value: "0", type: "number", span: 2 },
  { label: ".", value: ".", type: "number" },
  { label: "=", value: "=", type: "equals" },
];

function formatDisplay(value: string): string {
  if (value === "Error") return value;
  const num = parseFloat(value);
  if (isNaN(num)) return value;
  if (Math.abs(num) > 1e12 || (Math.abs(num) < 1e-6 && num !== 0)) {
    return num.toExponential(4);
  }
  const parts = value.split(".");
  const intPart = parts[0].replace(/^-?/, (sign) => {
    return sign + parseInt(parts[0].replace("-", ""), 10)
      .toLocaleString("en-US")
      .replace(/,/g, ",");
  });
  return intPart + (parts[1] !== undefined ? "." + parts[1] : "");
}

function formatNumber(n: number): string {
  const s = String(n);
  if (s.includes("e")) return s;
  return s;
}

export default function App() {
  const [display, setDisplay] = useState("0");
  const [prev, setPrev] = useState<string | null>(null);
  const [operator, setOperator] = useState<string | null>(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);
  const [expression, setExpression] = useState("");

  const inputDigit = (digit: string) => {
    if (waitingForOperand) {
      setDisplay(digit);
      setWaitingForOperand(false);
    } else {
      setDisplay(display === "0" ? digit : display + digit);
    }
  };

  const inputDecimal = () => {
    if (waitingForOperand) {
      setDisplay("0.");
      setWaitingForOperand(false);
      return;
    }
    if (!display.includes(".")) {
      setDisplay(display + ".");
    }
  };

  const clear = () => {
    setDisplay("0");
    setPrev(null);
    setOperator(null);
    setWaitingForOperand(false);
    setExpression("");
  };

  const negate = () => {
    const val = parseFloat(display);
    if (val !== 0) setDisplay(formatNumber(-val));
  };

  const percent = () => {
    const val = parseFloat(display);
    setDisplay(formatNumber(val / 100));
  };

  const handleOperator = (op: string) => {
    const current = parseFloat(display);
    if (prev !== null && operator && !waitingForOperand) {
      const result = calculate(parseFloat(prev), current, operator);
      const resultStr = formatNumber(result);
      setDisplay(resultStr);
      setPrev(resultStr);
      setExpression(resultStr + " " + opLabel(op));
    } else {
      setPrev(display);
      setExpression(display + " " + opLabel(op));
    }
    setOperator(op);
    setWaitingForOperand(true);
  };

  const opLabel = (op: string) => {
    switch (op) {
      case "/": return "÷";
      case "*": return "×";
      case "-": return "−";
      default: return op;
    }
  };

  const calculate = (a: number, b: number, op: string): number => {
    switch (op) {
      case "+": return a + b;
      case "-": return a - b;
      case "*": return a * b;
      case "/": return b === 0 ? NaN : a / b;
      default: return b;
    }
  };

  const handleEquals = () => {
    if (prev === null || operator === null) return;
    const current = parseFloat(display);
    const prevVal = parseFloat(prev);
    const result = calculate(prevVal, current, operator);
    const resultStr = isNaN(result) || !isFinite(result) ? "Error" : formatNumber(result);
    setExpression(prev + " " + opLabel(operator) + " " + display + " =");
    setDisplay(resultStr);
    setPrev(null);
    setOperator(null);
    setWaitingForOperand(true);
  };

  const handleButton = (btn: CalcButton) => {
    switch (btn.type) {
      case "number":
        if (btn.value === ".") inputDecimal();
        else inputDigit(btn.value);
        break;
      case "operator":
        handleOperator(btn.value);
        break;
      case "equals":
        handleEquals();
        break;
      case "clear":
        clear();
        break;
      case "special":
        if (btn.value === "negate") negate();
        else if (btn.value === "%") percent();
        break;
    }
  };

  const displayLength = display.replace("-", "").replace(".", "").length;
  const displaySize =
    displayLength > 12 ? "text-3xl" :
    displayLength > 9 ? "text-4xl" :
    displayLength > 6 ? "text-5xl" : "text-6xl";

  const buttonClass = (btn: CalcButton) => {
    const base =
      "flex items-center justify-center rounded-2xl font-semibold text-2xl select-none cursor-pointer transition-all duration-100 active:scale-95 h-20";
    if (btn.type === "operator") {
      return `${base} bg-purple-500 hover:bg-purple-400 text-white shadow-lg shadow-purple-500/30`;
    }
    if (btn.type === "equals") {
      return `${base} bg-purple-500 hover:bg-purple-400 text-white shadow-lg shadow-purple-500/30`;
    }
    if (btn.type === "clear" || btn.type === "special") {
      return `${base} bg-slate-600 hover:bg-slate-500 text-white`;
    }
    return `${base} bg-slate-700 hover:bg-slate-600 text-white`;
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-xs">
        <div className="mb-4 text-center">
          <h1 className="text-slate-400 text-sm font-medium tracking-widest uppercase mb-1">Calculator</h1>
        </div>

        <div className="bg-slate-800 rounded-3xl p-5 shadow-2xl shadow-black/40 border border-slate-700">
          {/* Display */}
          <div className="bg-slate-900 rounded-2xl p-4 mb-4 min-h-[110px] flex flex-col justify-end items-end overflow-hidden">
            <div className="text-slate-500 text-sm h-5 mb-1 truncate max-w-full text-right">
              {expression || "\u00A0"}
            </div>
            <div className={`text-white font-light leading-none truncate max-w-full ${displaySize}`}>
              {formatDisplay(display)}
            </div>
          </div>

          {/* Buttons */}
          <div className="grid grid-cols-4 gap-3">
            {buttons.map((btn, i) => (
              <button
                key={i}
                onClick={() => handleButton(btn)}
                className={`${buttonClass(btn)} ${btn.span === 2 ? "col-span-2" : ""}`}
              >
                {btn.label}
              </button>
            ))}
          </div>
        </div>

        <p className="text-center text-slate-500 text-xs mt-4">
          Tap the buttons to calculate
        </p>
      </div>
    </div>
  );
}
