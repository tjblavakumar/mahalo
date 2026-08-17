import { useEffect, useState } from 'react';
import { getPersonas, getSystemStatus, resetDemoData, sendMessage } from './services/api';

const starterMessages = [
  {
    role: 'assistant',
    content: 'MAHALO is ready. Ask about stories, incidents, or production signals.',
    agent: 'Orchestrator',
  },
];

function App() {
  const [personas, setPersonas] = useState([]);
  const [persona, setPersona] = useState('Executive');
  const [messages, setMessages] = useState(starterMessages);
  const [draft, setDraft] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [status, setStatus] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([getPersonas(), getSystemStatus()])
      .then(([personaData, statusData]) => {
        setPersonas(personaData.personas || []);
        setStatus(statusData);
      })
      .catch(() => setError('The API is offline. Start the MAHALO services and try again.'));
  }, []);

  async function submitMessage(event) {
    event.preventDefault();
    const message = draft.trim();
    if (!message || busy) return;

    setError('');
    setDraft('');
    setMessages((current) => [...current, { role: 'user', content: message, persona }]);
    setBusy(true);
    try {
      const result = await sendMessage({ persona, message, conversation_id: conversationId });
      setConversationId(result.conversation_id);
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: result.response, agent: (result.agents_used || []).join(', ') },
      ]);
    } catch (requestError) {
      setError(requestError.message || 'Unable to reach the MAHALO API.');
    } finally {
      setBusy(false);
    }
  }

  async function resetDemo() {
    setError('');
    try {
      await resetDemoData();
      setMessages(starterMessages);
      setConversationId(null);
      setStatus(await getSystemStatus());
    } catch (requestError) {
      setError(requestError.message || 'Demo reset failed.');
    }
  }

  const healthyServices = status?.healthy_services ?? 0;
  const totalServices = status?.total_services ?? 0;

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-mark">M</div>
        <div className="brand-copy">
          <p className="eyebrow">MAHALO / 01</p>
          <h1>Controls</h1>
          <p className="muted">One conversation across the delivery stack.</p>
        </div>

        <section className="sidebar-section">
          <div className="section-label">Your lens</div>
          <div className="persona-list">
            {(personas.length ? personas : [{ id: 'Executive', name: 'Executive' }]).map((item) => (
              <button
                className={`persona-option ${persona === item.id ? 'selected' : ''}`}
                key={item.id}
                onClick={() => setPersona(item.id)}
                type="button"
              >
                <span className="persona-dot" />
                <span>{item.name}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="sidebar-section status-panel">
          <div className="section-label">System pulse</div>
          <div className="pulse-line">
            <span className={`pulse-dot ${status?.overall_status === 'healthy' ? 'online' : ''}`} />
            <strong>{status?.overall_status || 'checking'}</strong>
          </div>
          <p className="muted">{healthyServices} of {totalServices || '...'} services reporting</p>
          <button className="text-button" onClick={resetDemo} type="button">Reset demo data</button>
        </section>

        <div className="sidebar-footer">MahaloPay / local prototype<br />API gateway :8000</div>
      </aside>

      <section className="workspace">
        <header className="workspace-header">
          <div>
            <p className="eyebrow">Live workspace</p>
            <h2>MAHALO: End To End AI SDLC assistant</h2>
          </div>
          <div className="header-meta">
            <span className="status-chip"><span className="pulse-dot online" /> Local mode</span>
            <span className="header-date">MahaloPay</span>
          </div>
        </header>

        <div className="conversation" aria-live="polite">
          {messages.map((message, index) => (
            <article className={`message-row ${message.role}`} key={`${message.role}-${index}`}>
              <div className="message-avatar">{message.role === 'assistant' ? 'M' : persona.slice(0, 1)}</div>
              <div className="message-body">
                <div className="message-meta">
                  <strong>{message.role === 'assistant' ? 'MAHALO' : message.persona || persona}</strong>
                  {message.agent && <span>{message.agent}</span>}
                </div>
                <p>{message.content}</p>
              </div>
            </article>
          ))}
          {busy && <div className="typing">MAHALO is tracing the request<span>.</span><span>.</span><span>.</span></div>}
        </div>

        <div className="composer-wrap">
          {error && <div className="error-banner">{error}</div>}
          <form className="composer" onSubmit={submitMessage}>
            <textarea
              aria-label="Message MAHALO"
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault();
                  event.currentTarget.form.requestSubmit();
                }
              }}
              placeholder={`Ask as ${persona}...`}
              rows="1"
              value={draft}
            />
            <button className="send-button" disabled={busy || !draft.trim()} type="submit">Send <span>↗</span></button>
          </form>
          <p className="composer-hint">Enter to send / Shift + Enter for a new line</p>
        </div>
      </section>
    </main>
  );
}

export default App;
