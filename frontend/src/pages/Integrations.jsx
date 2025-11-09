import React from 'react';

const integrations = [
  {
    name: 'ElevenLabs',
    id: 'elevenlabs',
    description: 'Generate realistic AI voices for documentation narration, tutorials, and accessibility layers.',
    site: 'https://elevenlabs.io',
    logo: 'https://seeklogo.com/images/E/elevenlabs-logo-270FE657B2-seeklogo.com.png',
    status: 'beta',
    category: 'AI Voice',
  },
  {
    name: 'Perplexity AI',
    id: 'perplexity',
    description: 'Accelerated research assistant that enriches docs with up-to-date contextual summaries.',
    site: 'https://www.perplexity.ai',
    logo: 'https://avatars.githubusercontent.com/u/123227139?s=200&v=4',
    status: 'planned',
    category: 'AI Research',
  },
  {
    name: 'Builder.io',
    id: 'builderio',
    description: 'Visual headless CMS for embedding live UI components and marketing sections in docs.',
    site: 'https://www.builder.io',
    logo: 'https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01bY6N8v2YsQv%2F2b2cc74d11d9451991b095447ddb5d10',
    status: 'alpha',
    category: 'Headless CMS',
  },
  {
    name: 'OpenAI Assistants',
    id: 'openai',
    description: 'Structured multi-turn assistants for context-aware doc generation and code explanation.',
    site: 'https://platform.openai.com',
    logo: 'https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg',
    status: 'enabled',
    category: 'LLM',
  },
  {
    name: 'Supabase',
    id: 'supabase',
    description: 'Edge-enabled Postgres and auth for storing project metadata and agent state.',
    site: 'https://supabase.com',
    logo: 'https://seeklogo.com/images/S/supabase-logo-DCC676FFE2-seeklogo.com.png',
    status: 'enabled',
    category: 'Database',
  },
  {
    name: 'Hugging Face',
    id: 'huggingface',
    description: 'Open models and embeddings powering semantic search across generated docs.',
    site: 'https://huggingface.co',
    logo: 'https://huggingface.co/front/assets/huggingface_logo.svg',
    status: 'planned',
    category: 'Models',
  },
];

const badgeColor = (status) => {
  switch (status) {
    case 'enabled': return 'bg-[#76B900]/20 text-[#76B900] border-[#76B900]/30';
    case 'beta': return 'bg-blue-900/30 text-blue-300 border-blue-700/40';
    case 'alpha': return 'bg-purple-900/30 text-purple-300 border-purple-700/40';
    case 'planned': return 'bg-gray-800 text-gray-400 border-gray-700';
    default: return 'bg-gray-800 text-gray-400 border-gray-700';
  }
};

const Integrations = () => {
  return (
    <div className="px-6 lg:px-8 max-w-7xl mx-auto py-10 animate-fade-in">
      <div className="mb-10">
        <h1 className="text-3xl font-semibold text-white mb-2">Integrations</h1>
        <p className="text-gray-400 max-w-2xl text-sm">Connect external AI, content, and infrastructure providers to extend the AutoDoc agent network.</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {integrations.map((i) => (
          <div key={i.id} className="group relative bg-[#0a0a0a] border border-gray-800 rounded-lg p-5 flex flex-col hover:border-[#76B900]/50 transition-colors">
            <div className="flex items-start gap-4 mb-4">
              <div className="w-12 h-12 rounded-md bg-black border border-gray-800 flex items-center justify-center overflow-hidden">
                <img src={i.logo} alt={i.name + ' logo'} className="w-10 h-10 object-contain" loading="lazy" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h2 className="text-white text-lg font-medium leading-tight">{i.name}</h2>
                  <span className={`text-[10px] px-2 py-1 rounded-md border font-medium tracking-wide ${badgeColor(i.status)}`}>{i.status.toUpperCase()}</span>
                </div>
                <div className="text-xs text-gray-500 mt-0.5">{i.category}</div>
              </div>
            </div>
            <p className="text-sm text-gray-300 leading-relaxed flex-1 mb-4 line-clamp-4">{i.description}</p>
            <div className="flex items-center justify-between mt-auto pt-2">
              <a href={i.site} target="_blank" rel="noreferrer" className="text-xs text-[#76B900] hover:underline flex items-center gap-1">
                Visit Site
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h6m0 0v6m0-6l-9 9" />
                </svg>
              </a>
              <button className="text-xs px-3 py-1.5 rounded-md bg-gray-900 border border-gray-800 text-gray-300 hover:border-[#76B900]/50 hover:text-white transition">Connect</button>
            </div>
            <div className="absolute inset-0 rounded-lg ring-0 group-hover:ring-1 ring-[#76B900]/40 pointer-events-none transition" />
          </div>
        ))}
      </div>

      <div className="mt-12 border border-dashed border-gray-800 rounded-lg p-6 text-center">
        <h3 className="text-white font-medium mb-2">Need another integration?</h3>
        <p className="text-xs text-gray-400 mb-4">We prioritize based on community requests. Submit a provider and we will explore adding an agent.</p>
        <button className="px-4 py-2 text-xs font-medium rounded-md bg-[#76B900] text-black hover:bg-[#5d9100] transition">Request Integration</button>
      </div>
    </div>
  );
};

export default Integrations;
