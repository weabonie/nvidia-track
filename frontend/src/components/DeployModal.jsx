import { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card } from "./ui/card";

export const DeployModal = ({ isOpen, onClose }) => {
  const [githubUrl, setGithubUrl] = useState('');
  // Overall deploying/waiting state (spinner + countdown UI)
  const [ingestLoading, setIngestLoading] = useState(false);
  const [ingestData, setIngestData] = useState(null);
  const [ingestError, setIngestError] = useState(null);
  const [ingestAbortController, setIngestAbortController] = useState(null);
  const [ingestCompleted, setIngestCompleted] = useState(false);
  const [deployStartTime, setDeployStartTime] = useState(null);
  const [elapsedMs, setElapsedMs] = useState(0);
  // Enforce a minimum wait time of 5 minutes (300000 ms)
  const MIN_WAIT_MS = 5 * 60 * 1000;
  const [minWaitUntil, setMinWaitUntil] = useState(null);
  const [finishNow, setFinishNow] = useState(false);

  // Update elapsed time while loading
  useEffect(() => {
    if (!ingestLoading) {
      setElapsedMs(0);
      return;
    }
    const id = setInterval(() => {
      setElapsedMs(Date.now() - (deployStartTime || Date.now()));
    }, 1000);
    return () => clearInterval(id);
  }, [ingestLoading, deployStartTime]);

  // When backend completes, continue showing loader until min wait is over, unless user clicks Finish Now
  useEffect(() => {
    if (!ingestLoading || !minWaitUntil) return;
    let rafId;
    const tick = () => {
      const now = Date.now();
      const minWaitOver = now >= minWaitUntil;
      if ((ingestCompleted && minWaitOver) || (ingestCompleted && finishNow)) {
        setIngestLoading(false); // move to completed UI
        return;
      }
      rafId = requestAnimationFrame(tick);
    };
    rafId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafId);
  }, [ingestLoading, minWaitUntil, ingestCompleted, finishNow]);

  // Handle Escape key to close modal
  useEffect(() => {
    if (!isOpen) return;
    
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        handleClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const handleDeploy = async (e) => {
    e.preventDefault();
    if (githubUrl.trim()) {
      // Call backend ingest endpoint to retrieve project metadata
      const controller = new AbortController();
      setIngestAbortController(controller);
      setDeployStartTime(Date.now());
      setIngestCompleted(false);
      setFinishNow(false);
      setMinWaitUntil(Date.now() + MIN_WAIT_MS);
      
      try {
        setIngestLoading(true);
        setIngestError(null);
        const resp = await axios.get("https://apihackutd.siru.dev/ingest", {
          params: { repo_url: githubUrl.trim() },
          signal: controller.signal,
        });
        console.log("Ingest response:", resp.data);
        setIngestData(resp.data);
        setIngestCompleted(true);
        // Clear the input so user can add another later
        setGithubUrl("");
      } catch (err) {
        console.error("Ingest failed", err);
        const message = err?.name === 'CanceledError' || err?.code === 'ERR_CANCELED' 
          ? 'Deploy cancelled' 
          : (err?.message || "Failed to ingest repository");
        setIngestError(message);
        // Stop loading if there was an error
        setIngestLoading(false);
      } finally {
        setIngestAbortController(null);
      }
    }
  };

  const cancelDeploy = () => {
    if (ingestAbortController) {
      try {
        ingestAbortController.abort();
      } catch (e) {
        // ignore
      }
    }
    setIngestLoading(false);
    setIngestAbortController(null);
    setIngestError('Deploy cancelled');
    setIngestCompleted(false);
    setMinWaitUntil(null);
    setFinishNow(false);
  };

  const handleClose = () => {
    if (ingestLoading) {
      cancelDeploy();
    }
    setGithubUrl('');
    setIngestError(null);
    setIngestData(null);
    setIngestCompleted(false);
    setMinWaitUntil(null);
    setFinishNow(false);
    onClose();
  };

  const formatElapsedTime = (ms) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`;
    }
    return `${seconds}s`;
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/80 backdrop-blur-sm animate-fade-in"
      onClick={() => handleClose()}
    >
      <div
        className="w-full max-w-lg bg-[#0a0a0a] border border-gray-800 rounded-md shadow-2xl animate-scale-in"
        onClick={(e) => e.stopPropagation()}
      >
            {/* Header */}
            <div className="px-6 py-4 border-b border-gray-800">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-white">Deploy New Project</h2>
                <button
                  onClick={handleClose}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Content */}
            {!(ingestLoading || ingestCompleted || ingestError) ? (
              <form onSubmit={handleDeploy} className="p-6">
              <div className="mb-6">
                <label htmlFor="github-url" className="block text-sm font-medium text-gray-300 mb-2">
                  GitHub Repository URL
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg className="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                      <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <input
                    type="text"
                    id="github-url"
                    value={githubUrl}
                    onChange={(e) => setGithubUrl(e.target.value)}
                    placeholder="https://github.com/username/repository"
                    className="w-full pl-10 pr-4 py-2.5 bg-black border border-gray-800 rounded-md text-white placeholder-gray-600 focus:outline-none focus:border-[#76B900] transition-colors"
                    required
                  />
                </div>
                <p className="mt-2 text-xs text-gray-500">
                  Enter the full URL of your GitHub repository to deploy
                </p>
              </div>

              {/* Framework Detection */}
              <div className="mb-6 p-4 bg-gray-900/50 border border-gray-800 rounded-md">
                <div className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-[#76B900] mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <p className="text-sm text-white font-medium mb-1">Auto-detect Framework</p>
                    <p className="text-xs text-gray-400">
                      AutoDoc will automatically detect your framework and configure build settings
                    </p>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={handleClose}
                  className="flex-1 px-4 py-2.5 text-sm font-medium text-gray-300 bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-md transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2.5 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={!githubUrl.trim() || ingestLoading}
                >
                  {ingestLoading ? "Deploying..." : "Deploy"}
                </button>
              </div>
              </form>
            ) : (
              <div className="p-6">
                {ingestLoading && (
                  <div className="flex flex-col gap-4">
                    <div className="flex items-center gap-4">
                      <svg className="w-6 h-6 animate-spin text-white" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" className="opacity-20" />
                        <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" strokeWidth="4" strokeLinecap="round" className="opacity-100" />
                      </svg>
                      <div>
                        <div className="text-white font-medium">Deploying project…</div>
                        <div className="text-xs text-gray-400">Elapsed: {Math.floor(elapsedMs/1000)}s</div>
                        {minWaitUntil && (
                          <div className="text-xs text-gray-400">
                            Minimum time remaining: {Math.max(0, Math.ceil((minWaitUntil - Date.now())/1000))}s
                          </div>
                        )}
                        {ingestCompleted && !finishNow && (
                          <div className="text-xs text-gray-400 mt-1">Backend finished. Finalizing deployment…</div>
                        )}
                      </div>
                    </div>
                    {minWaitUntil && (
                      <div className="w-full h-2 bg-gray-800 rounded">
                        <div
                          className="h-2 bg-[#76B900] rounded transition-all"
                          style={{ width: `${Math.min(100, Math.floor(((elapsedMs) / MIN_WAIT_MS) * 100))}%` }}
                        />
                      </div>
                    )}
                    <div className="flex gap-2">
                      <button onClick={() => { cancelDeploy(); handleClose(); }} className="px-4 py-2 text-sm bg-gray-900 text-gray-300 rounded-md">Cancel</button>
                      {ingestCompleted ? (
                        <button onClick={() => setFinishNow(true)} className="px-4 py-2 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">Finish Now</button>
                      ) : (
                        <button onClick={() => { /* keep modal open */ }} className="px-4 py-2 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">Keep Open</button>
                      )}
                    </div>
                  </div>
                )}

                {ingestCompleted && ingestData && (
                  <div className="flex flex-col gap-4">
                    <div className="text-white font-medium">Deploy completed successfully</div>
                    <div className="text-sm text-gray-300">Project: <strong>{ingestData.name || ingestData['repo-name']}</strong></div>
                    {ingestData.doc_generation?.response?.url && (
                      <a href={ingestData.doc_generation.response.url} target="_blank" rel="noreferrer" className="text-sm text-[#76B900] underline">Open generated site</a>
                    )}
                    <div className="flex gap-2">
                      <button onClick={handleClose} className="px-4 py-2 text-sm bg-[#76B900] text-black rounded-md">Close</button>
                      <button onClick={handleClose} className="px-4 py-2 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">View Project</button>
                    </div>
                  </div>
                )}

                {ingestError && (
                  <div className="flex flex-col gap-4">
                    <div className="text-white font-medium">Deploy failed</div>
                    <div className="text-sm text-red-400">{ingestError}</div>
                    <div className="flex gap-2">
                      <button onClick={() => { setIngestError(null); setIngestData(null); setIngestCompleted(false); }} className="px-4 py-2 text-sm bg-gray-900 text-gray-300 rounded-md">Retry</button>
                      <button onClick={handleClose} className="px-4 py-2 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">Close</button>
                    </div>
                  </div>
                )}
              </div>
            )}
      </div>
    </div>
  );
};

export default DeployModal;