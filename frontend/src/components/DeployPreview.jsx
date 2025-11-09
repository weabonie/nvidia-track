import { useState } from 'react';
import { Card } from "./ui/card";

export const DeployPreview = ({ className = "" }) => {
  const [isTyping, setIsTyping] = useState(true);
  const [text, setText] = useState("");
  const demoUrl = "github.com/nvidia/docs-project";

  // Simulated typing effect
  useState(() => {
    let currentText = "";
    const fullText = demoUrl;
    let currentIndex = 0;

    const typeInterval = setInterval(() => {
      if (currentIndex < fullText.length) {
        currentText += fullText[currentIndex];
        setText(currentText);
        currentIndex++;
      } else {
        setIsTyping(false);
        clearInterval(typeInterval);
      }
    }, 100);

    return () => clearInterval(typeInterval);
  }, []);

  return (
    <Card className={`w-full max-w-lg bg-gray-900/90 border border-gray-800 shadow-2xl ${className}`}>
      <div className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <div className="text-sm text-gray-500">Deploy Project</div>
        </div>
        
        <div className="space-y-4">
          <div className="bg-black/50 border border-gray-700 rounded-lg p-3">
            <div className="text-gray-400 text-sm mb-2">Repository URL</div>
            <div className="font-mono text-[#76B900]">
              {text}
              {isTyping && <span className="animate-pulse">|</span>}
            </div>
          </div>
          
          <div className="bg-black/30 border border-gray-800 rounded-lg p-3">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-[#76B900] animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span className="text-sm text-gray-400">Processing repository...</span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default DeployPreview;