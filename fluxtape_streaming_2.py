import streamlit as st
import json
import random

st.set_page_config(layout="wide", page_title="FluXTape", page_icon="🎵")

# Custom CSS - minimal and clean
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"] {
  background: rgba(0,0,0,0) !important;
}
[data-testid="stSidebar"] {
  background: rgba(0,0,0,0.15) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

* {
  font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
  color: #ffffff !important;
  font-family: 'Inter', sans-serif !important;
}

.track-card {
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
  padding: 25px;
  margin: 20px auto;
  max-width: 800px;
  border: 1px solid rgba(255,255,255,0.05);
}

.version-badge {
  background: rgba(95, 107, 255, 0.15);
  color: #8b9dff;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  display: inline-block;
  margin: 5px 3px;
}

.rank-badge {
  background: rgba(139, 146, 168, 0.2);
  color: #8b92a8;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
  display: inline-block;
}

.feature-tag {
  background: rgba(255,255,255,0.05);
  color: #8b92a8;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 400;
  display: inline-block;
  margin: 2px;
}

.research-banner {
  background: rgba(95, 107, 255, 0.05);
  border: 1px solid rgba(95, 107, 255, 0.2);
  border-radius: 8px;
  padding: 20px;
  margin: 20px auto;
  max-width: 700px;
}

.stButton button {
  background: rgba(255,255,255,0.08) !important;
  color: #ffffff !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 6px !important;
  padding: 10px 24px !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  transition: all 0.2s ease !important;
}

.stButton button:hover {
  background: rgba(255,255,255,0.12) !important;
  border-color: rgba(255,255,255,0.2) !important;
}

p, label, div {
  color: #8b92a8 !important;
}
</style>
""", unsafe_allow_html=True)

# Mock data - simulating different contributor versions with rankings
versions = [
    {
        "id": 1,
        "contributor": "@contributor_01",
        "rank": 1,
        "preference_score": 847,
        "features": {
            "lyrics": "A",
            "groove": "B",
            "solo": "A",
            "spatialize": "wide",
            "backing_vocals": "on"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/groove.mp3"
    },
    {
        "id": 2,
        "contributor": "@contributor_02",
        "rank": 2,
        "preference_score": 623,
        "features": {
            "lyrics": "C",
            "groove": "A",
            "solo": "B",
            "spatialize": "narrow",
            "backing_vocals": "off"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/groove.mp3"
    },
    {
        "id": 3,
        "contributor": "@contributor_03",
        "rank": 3,
        "preference_score": 501,
        "features": {
            "lyrics": "B",
            "groove": "C",
            "solo": "A",
            "spatialize": "wide",
            "backing_vocals": "on"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/groove.mp3"
    },
    {
        "id": 4,
        "contributor": "@contributor_04",
        "rank": 4,
        "preference_score": 389,
        "features": {
            "lyrics": "A",
            "groove": "A",
            "solo": "B",
            "spatialize": "narrow",
            "backing_vocals": "on"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/groove.mp3"
    },
    {
        "id": 5,
        "contributor": "@contributor_05",
        "rank": 5,
        "preference_score": 267,
        "features": {
            "lyrics": "B",
            "groove": "B",
            "solo": "A",
            "spatialize": "wide",
            "backing_vocals": "off"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/groove.mp3"
    }
]

# Probabilistic selection based on rank
def select_version_probabilistically(versions):
    """Select a version based on inverse rank weighting"""
    weights = [1.0 / v['rank'] for v in versions]
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    
    selected = random.choices(versions, weights=normalized_weights, k=1)[0]
    return selected

# Initialize session state
if 'current_version' not in st.session_state:
    st.session_state.current_version = select_version_probabilistically(versions)
if 'play_count' not in st.session_state:
    st.session_state.play_count = 0
if 'version_history' not in st.session_state:
    st.session_state.version_history = []

# Header
st.markdown("""
<div style="text-align:center; margin-bottom:25px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:700; color:#ffffff; font-size:36px; margin-bottom:8px; letter-spacing:-0.5px;">
    FluXTape Research Platform
  </h1>
  <p style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:14px; margin-top:0;">
    Exploring Musical Variation and Listener Preference
  </p>
</div>
""", unsafe_allow_html=True)

# Research context banner
st.markdown("""
<div class="research-banner">
  <div style="color:#ffffff; font-size:13px; font-weight:600; margin-bottom:10px;">
    Research Study: Musical Version Preference
  </div>
  <div style="color:#8b92a8; font-size:12px; line-height:1.6;">
    This platform investigates how listeners respond to musical variations within the same song. 
    Each playback presents a different community-created version, selected probabilistically based on 
    aggregate listener preferences. Your interactions help us understand patterns in musical taste.
  </div>
</div>
""", unsafe_allow_html=True)

# Track info
st.markdown("""
<div class="track-card">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div>
      <h2 style="margin:0; font-size:22px; color:#ffffff; font-weight:600;">Mid-nite Free-Quensee</h2>
      <p style="margin:5px 0 0 0; font-size:14px; color:#8b92a8;">Original Artist: Zlisterr</p>
    </div>
    <div style="text-align:right;">
      <div style="color:#8b92a8; font-size:11px; margin-bottom:5px;">Study Versions</div>
      <div style="color:#ffffff; font-size:14px; font-weight:500;">N = {}</div>
    </div>
  </div>
</div>
""".format(len(versions) * 167), unsafe_allow_html=True)  # Simulating 837 versions

# Current version playing
current = st.session_state.current_version

st.markdown(f"""
<div class="track-card" style="border: 1px solid rgba(95, 107, 255, 0.2);">
  <div style="text-align:center; margin-bottom:15px;">
    <div style="color:#8b92a8; font-size:11px; margin-bottom:8px; letter-spacing:0.5px;">CURRENTLY PLAYING</div>
    <div style="font-size:16px; color:#ffffff; font-weight:500; margin-bottom:8px;">
      Version {current['id']} by {current['contributor']}
    </div>
    <span class="rank-badge">Rank #{current['rank']}</span>
    <span class="version-badge">Preference Score: {current['preference_score']}</span>
  </div>
  
  <div style="margin:15px 0; text-align:center;">
    <div style="color:#8b92a8; font-size:11px; margin-bottom:8px;">FEATURE COMBINATION:</div>
    <span class="feature-tag">Lyrics {current['features']['lyrics']}</span>
    <span class="feature-tag">Groove {current['features']['groove']}</span>
    <span class="feature-tag">Solo {current['features']['solo']}</span>
    <span class="feature-tag">{current['features']['spatialize'].title()}</span>
    <span class="feature-tag">BG Vocals {current['features']['backing_vocals'].title()}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Audio player
audio_html = f"""
<div style="text-align:center; margin:25px auto; max-width:800px;">
  <div id="waveform" style="margin:15px 0;"></div>
  
  <div style="margin:15px 0;">
    <button id="playBtn" class="play-btn" title="Play/Pause">▶</button>
  </div>
  
  <div id="time-display" style="color:#8b92a8; font-family:monospace; font-size:14px; font-weight:500; margin:10px 0;">
    0:00 / 0:00
  </div>
  
  <div style="margin:15px auto; max-width:350px;">
    <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="0.8" class="slider">
  </div>
</div>

<style>
  .play-btn {{
    width: 70px;
    height: 70px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.1);
    font-size: 28px;
    cursor: pointer;
    color: #fff;
    background: rgba(255,255,255,0.08);
    transition: all 0.2s ease;
  }}
  .play-btn:hover {{ 
    background: rgba(255,255,255,0.12);
  }}
  .play-btn.pause {{
    background: rgba(255,255,255,0.1);
  }}
  
  .slider {{
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 4px;
    border-radius: 2px;
    background: rgba(255,255,255,0.1);
    outline: none;
  }}
  
  .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #ffffff;
    cursor: pointer;
  }}
  
  .slider::-moz-range-thumb {{
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #ffffff;
    cursor: pointer;
    border: none;
  }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7.7.3"></script>
<script>
  const audioUrl = '{current["audio_url"]}';
  
  const wavesurfer = WaveSurfer.create({{
    container: '#waveform',
    waveColor: 'rgba(139, 146, 168, 0.3)',
    progressColor: 'rgba(139, 146, 168, 0.7)',
    cursorColor: '#ffffff',
    barWidth: 2,
    barRadius: 2,
    cursorWidth: 1,
    height: 60,
    barGap: 2,
    backend: 'WebAudio',
    normalize: true
  }});
  
  wavesurfer.load(audioUrl);
  
  const playBtn = document.getElementById('playBtn');
  const timeDisplay = document.getElementById('time-display');
  const volumeSlider = document.getElementById('volumeSlider');
  
  let isPlaying = false;
  
  playBtn.addEventListener('click', () => {{
    wavesurfer.playPause();
    isPlaying = !isPlaying;
    playBtn.textContent = isPlaying ? '⏸' : '▶';
    playBtn.classList.toggle('pause', isPlaying);
  }});
  
  volumeSlider.addEventListener('input', (e) => {{
    wavesurfer.setVolume(parseFloat(e.target.value));
  }});
  
  function formatTime(seconds) {{
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
  }}
  
  wavesurfer.on('audioprocess', () => {{
    const current = wavesurfer.getCurrentTime();
    const duration = wavesurfer.getDuration();
    timeDisplay.textContent = `${{formatTime(current)}} / ${{formatTime(duration)}}`;
  }});
  
  wavesurfer.on('ready', () => {{
    const duration = wavesurfer.getDuration();
    timeDisplay.textContent = `0:00 / ${{formatTime(duration)}}`;
  }});
  
  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === ' ') {{
      e.preventDefault();
      playBtn.click();
    }}
  }});
</script>
"""

st.components.v1.html(audio_html, height=280)

# Interaction buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⏭ Next Version", use_container_width=True):
        st.session_state.version_history.append(st.session_state.current_version['id'])
        st.session_state.current_version = select_version_probabilistically(versions)
        st.session_state.play_count += 1
        st.rerun()

with col2:
    if st.button("⭐ Prefer This Version", use_container_width=True):
        st.session_state.version_history.append(st.session_state.current_version['id'])
        st.success(f"Preference recorded for Version {current['id']}")

with col3:
    if st.button("📊 View All Versions", use_container_width=True):
        st.info("Full version comparison available in extended study interface")

# Research questions section
st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)

with st.expander("**Research Questions & Methodology**", expanded=False):
    st.markdown("""
    <div style="color:#8b92a8; font-size:13px; line-height:1.7;">
        <p><strong style="color:#ffffff;">Primary Research Questions:</strong></p>
        <ul>
            <li>Do listeners consistently prefer certain lyrical/instrumental combinations?</li>
            <li>Is there such a thing as a "best version" for most people, or does preference vary widely?</li>
            <li>How does familiarity with the song influence version preference?</li>
            <li>Can understanding these patterns inform songwriting, arrangement, or production practices?</li>
        </ul>
        
        <p style="margin-top:20px;"><strong style="color:#ffffff;">Methodology:</strong></p>
        <ul>
            <li><strong>Version Selection:</strong> Probabilistic sampling weighted by aggregate preference scores</li>
            <li><strong>Feature Tracking:</strong> Each version represents unique combinations of stems (vocals, instruments, spatial mix)</li>
            <li><strong>Preference Collection:</strong> Implicit (listening duration) and explicit (preference marking) data</li>
            <li><strong>Analysis Focus:</strong> Pattern identification in feature combinations, ranking stability, convergence/divergence of preferences</li>
        </ul>
        
        <p style="margin-top:20px; font-size:12px; font-style:italic;">
            This research builds on findings from "How Much Lyrics Matter" (2024), which identified emotional 
            asymmetries in lyric-music interactions. The current study extends this to explore multi-dimensional 
            variation in full musical arrangements.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Stats section - reframed as research data
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:rgba(255,255,255,0.03); border-radius:8px;">
        <div style="font-size:24px; color:#8b92a8; font-weight:600; margin-bottom:5px;">837</div>
        <div style="font-size:10px; color:#6b7280; letter-spacing:0.5px;">VERSIONS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:rgba(255,255,255,0.03); border-radius:8px;">
        <div style="font-size:24px; color:#8b92a8; font-weight:600; margin-bottom:5px;">12.4K</div>
        <div style="font-size:10px; color:#6b7280; letter-spacing:0.5px;">LISTENING SESSIONS</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:rgba(255,255,255,0.03); border-radius:8px;">
        <div style="font-size:24px; color:#8b92a8; font-weight:600; margin-bottom:5px;">432</div>
        <div style="font-size:10px; color:#6b7280; letter-spacing:0.5px;">CONTRIBUTORS</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:rgba(255,255,255,0.03); border-radius:8px;">
        <div style="font-size:24px; color:#8b92a8; font-weight:600; margin-bottom:5px;">14</div>
        <div style="font-size:10px; color:#6b7280; letter-spacing:0.5px;">DAYS ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)

# Top-ranked versions (minimal presentation)
st.markdown("<h3 style='margin-top:40px; text-align:center; font-size:18px; color:#ffffff; font-weight:500;'>Most Preferred Versions</h3>", unsafe_allow_html=True)

for i, version in enumerate(versions[:5]):
    highlight = "border-left: 2px solid rgba(95, 107, 255, 0.3);" if version['id'] == current['id'] else ""
    st.markdown(f"""
    <div style="padding:12px 15px; margin:8px auto; max-width:650px; background:rgba(255,255,255,0.02); border-radius:6px; {highlight}">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="font-size:14px; color:#8b92a8; font-weight:500; min-width:30px;">#{version['rank']}</div>
                <div>
                    <div style="font-size:13px; color:#ffffff; font-weight:500;">{version['contributor']}</div>
                    <div style="font-size:10px; color:#6b7280; margin-top:2px;">
                        {version['features']['lyrics']} • {version['features']['groove']} • {version['features']['spatialize']}
                    </div>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="color:#8b92a8; font-weight:500; font-size:12px;">{version['preference_score']}</div>
                <div style="color:#6b7280; font-size:9px;">preference score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer - research context
st.markdown("""
<div style="text-align:center; margin-top:50px; padding:25px; background:rgba(255,255,255,0.02); border-radius:8px;">
  <div style="color:#8b92a8; font-size:11px; font-family:'Inter', sans-serif; line-height:1.7;">
    <strong style="color:#ffffff;">About This Study</strong><br><br>
    FluXTape is a research platform developed at Georgia Institute of Technology investigating 
    the relationship between musical variation and listener preference. By allowing multiple 
    community-created versions of the same song to coexist, this platform generates data on 
    how listeners respond to different combinations of musical elements.<br><br>
    
    Each playback presents a version selected probabilistically based on cumulative preference scores, 
    enabling observation of both individual choices and emergent collective patterns.<br><br>
    
    <span style="font-size:10px; color:#6b7280;">
    Platform designed by Peyman Kohsarnia • CCML Lab • Georgia Institute of Technology
    </span>
  </div>
</div>
""", unsafe_allow_html=True)