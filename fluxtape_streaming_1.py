
import streamlit as st
import json
import random

st.set_page_config(layout="wide", page_title="FluXTape Stream", page_icon="🎵")

# Custom CSS matching REF 7 aesthetic
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

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
  border-radius: 16px;
  padding: 30px;
  margin: 20px auto;
  max-width: 800px;
  border: 1px solid rgba(255,255,255,0.05);
}

.version-badge {
  background: rgba(76, 175, 80, 0.2);
  color: #66BB6A;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: inline-block;
  margin: 10px 5px;
}

.rank-badge {
  background: rgba(251, 192, 45, 0.2);
  color: #FDD835;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: inline-block;
}

.feature-tag {
  background: rgba(95, 107, 255, 0.15);
  color: #5f6bff;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
  display: inline-block;
  margin: 3px;
}

.subscribe-banner {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(95, 107, 255, 0.1) 100%);
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  padding: 20px;
  margin: 30px auto;
  max-width: 600px;
  text-align: center;
}

.stButton button {
  background: #4CAF50 !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 12px 32px !important;
  font-weight: 600 !important;
  font-size: 16px !important;
  transition: all 0.3s ease !important;
}

.stButton button:hover {
  background: #66BB6A !important;
  transform: scale(1.02);
}

p, label, div {
  color: #8b92a8 !important;
}
</style>
""", unsafe_allow_html=True)

# Mock data - simulating different contributor versions with rankings
# In production, this would come from your database
versions = [
    {
        "id": 1,
        "contributor": "@beatmaker_nova",
        "rank": 1,
        "votes": 847,
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
        "contributor": "@zlisterr_fan_42",
        "rank": 2,
        "votes": 623,
        "features": {
            "lyrics": "C",
            "groove": "A",
            "solo": "B",
            "spatialize": "narrow",
            "backing_vocals": "off"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsA.mp3"
    },
    {
        "id": 3,
        "contributor": "@studio_wizard",
        "rank": 3,
        "votes": 501,
        "features": {
            "lyrics": "B",
            "groove": "C",
            "solo": "A",
            "spatialize": "wide",
            "backing_vocals": "on"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsB.mp3"
    },
    {
        "id": 4,
        "contributor": "@soundscape_dreamer",
        "rank": 4,
        "votes": 389,
        "features": {
            "lyrics": "A",
            "groove": "A",
            "solo": "B",
            "spatialize": "narrow",
            "backing_vocals": "on"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsC.mp3"
    },
    {
        "id": 5,
        "contributor": "@mix_architect",
        "rank": 5,
        "votes": 267,
        "features": {
            "lyrics": "B",
            "groove": "B",
            "solo": "A",
            "spatialize": "wide",
            "backing_vocals": "off"
        },
        "audio_url": "https://raw.githubusercontent.com/theallophones/audio/main/soloA.mp3"
    }
]

# Probabilistic selection based on rank (higher rank = more likely)
def select_version_probabilistically(versions):
    """Select a version based on inverse rank weighting"""
    # Higher rank (lower number) gets more weight
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

# Header
st.markdown("""
<div style="text-align:center; margin-bottom:30px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:48px; margin-bottom:5px; letter-spacing:-1px;">
    FluX-Tape
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:16px; margin-top:0; letter-spacing:0.5px;">
    Songs as Probability Clouds
  </h3>
</div>
""", unsafe_allow_html=True)

# Track info
st.markdown("""
<div class="track-card">
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:20px;">
    <div>
      <h2 style="margin:0; font-size:28px; color:#ffffff;">Neon Dreams</h2>
      <p style="margin:5px 0 0 0; font-size:16px; color:#8b92a8;">by Zlisterr</p>
    </div>
    <div style="text-align:right;">
      <div style="color:#8b92a8; font-size:12px; margin-bottom:5px;">Contributor Period Ended</div>
      <div style="color:#4CAF50; font-size:14px; font-weight:600;">837 Community Versions</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Current version playing
current = st.session_state.current_version

st.markdown(f"""
<div class="track-card" style="border: 2px solid rgba(76, 175, 80, 0.2);">
  <div style="text-align:center; margin-bottom:20px;">
    <div style="color:#8b92a8; font-size:13px; margin-bottom:10px; letter-spacing:1px;">NOW STREAMING</div>
    <div style="font-size:20px; color:#ffffff; font-weight:600; margin-bottom:10px;">
      Version by {current['contributor']}
    </div>
    <span class="rank-badge">#{current['rank']} RANKED</span>
    <span class="version-badge">🔥 {current['votes']} votes</span>
  </div>
  
  <div style="margin:20px 0; text-align:center;">
    <div style="color:#8b92a8; font-size:12px; margin-bottom:10px;">THIS VERSION FEATURES:</div>
    <span class="feature-tag">Lyrics {current['features']['lyrics']}</span>
    <span class="feature-tag">Groove {current['features']['groove']}</span>
    <span class="feature-tag">Solo {current['features']['solo']}</span>
    <span class="feature-tag">{current['features']['spatialize'].title()} Mix</span>
    <span class="feature-tag">Backing Vocals {current['features']['backing_vocals'].title()}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Audio player (embedded HTML player)
audio_html = f"""
<div style="text-align:center; margin:30px auto; max-width:800px;">
  <div id="waveform" style="margin:20px 0;"></div>
  
  <div style="margin:20px 0;">
    <button id="playBtn" class="play-btn" title="Play/Pause">▶</button>
  </div>
  
  <div id="time-display" style="color:#ffffff; font-family:'JetBrains Mono', monospace; font-size:20px; font-weight:600; letter-spacing:2px; margin:15px 0;">
    0:00 / 0:00
  </div>
  
  <div style="margin:20px auto; max-width:400px;">
    <div style="color:#8b92a8; font-size:14px; margin-bottom:8px;">🔊 Volume</div>
    <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="0.8" class="slider">
  </div>
</div>

<style>
  .play-btn {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: none;
    font-size: 32px;
    cursor: pointer;
    color: #fff;
    background: #4CAF50;
    transition: all 0.3s ease;
    box-shadow: 0 8px 24px rgba(76,175,80,.5);
  }}
  .play-btn:hover {{ 
    transform: scale(1.08); 
    background: #66BB6A;
    box-shadow: 0 12px 32px rgba(76,175,80,.6);
  }}
  .play-btn:active {{ transform: scale(0.98); }}
  .play-btn.pause {{
    background: #FBC02D;
    box-shadow: 0 8px 24px rgba(251,192,45,.5);
  }}
  .play-btn.pause:hover {{
    background: #FDD835;
  }}
  
  .slider {{
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 6px;
    border-radius: 5px;
    background: linear-gradient(to right, #5f6bff 80%, #3a4150 80%);
    outline: none;
    transition: all 0.3s;
  }}
  
  .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #ffffff;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}
  
  .slider::-moz-range-thumb {{
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #ffffff;
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7.7.3"></script>
<script>
  const audioUrl = '{current["audio_url"]}';
  
  const wavesurfer = WaveSurfer.create({{
    container: '#waveform',
    waveColor: 'rgba(139, 146, 168, 0.5)',
    progressColor: '#4CAF50',
    cursorColor: '#66BB6A',
    barWidth: 2,
    barRadius: 3,
    cursorWidth: 1,
    height: 80,
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
    const vol = parseFloat(e.target.value);
    wavesurfer.setVolume(vol);
    const percent = vol * 100;
    volumeSlider.style.background = `linear-gradient(to right, #5f6bff ${{percent}}%, #3a4150 ${{percent}}%)`;
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
  
  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === ' ') {{
      e.preventDefault();
      playBtn.click();
    }}
    if (e.key === 'ArrowUp') {{
      e.preventDefault();
      const newVol = Math.min(1, parseFloat(volumeSlider.value) + 0.1);
      volumeSlider.value = newVol;
      volumeSlider.dispatchEvent(new Event('input'));
    }}
    if (e.key === 'ArrowDown') {{
      e.preventDefault();
      const newVol = Math.max(0, parseFloat(volumeSlider.value) - 0.1);
      volumeSlider.value = newVol;
      volumeSlider.dispatchEvent(new Event('input'));
    }}
  }});
  
  // Initialize slider gradient
  volumeSlider.style.background = 'linear-gradient(to right, #5f6bff 80%, #3a4150 80%)';
</script>
"""

st.components.v1.html(audio_html, height=400)

# Action buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔄 Next Random Version", use_container_width=True):
        st.session_state.current_version = select_version_probabilistically(versions)
        st.session_state.play_count += 1
        st.rerun()

with col2:
    if st.button("💾 Save This Version", use_container_width=True):
        st.info("Subscribe to save your favorite versions and create your own!")

with col3:
    if st.button("❤️ Like This Mix", use_container_width=True):
        st.success(f"Liked! +1 vote for {current['contributor']}")

# Subscribe banner
st.markdown("""
<div class="subscribe-banner">
  <div style="font-size:20px; color:#ffffff; font-weight:700; margin-bottom:10px;">
    🎚️ Want to Create Your Own Version?
  </div>
  <div style="color:#8b92a8; font-size:14px; margin-bottom:20px;">
    Upgrade to Contributor access and remix any track with full creative control.<br>
    Mix stems, upload your own parts, and compete for top rankings.
  </div>
  <button style="background:#4CAF50; color:white; border:none; padding:12px 32px; border-radius:8px; font-size:16px; font-weight:600; cursor:pointer;">
    Subscribe for $4.99/month
  </button>
</div>
""", unsafe_allow_html=True)

# Stats section
st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="text-align:center; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px;">
        <div style="font-size:28px; color:#4CAF50; font-weight:700; margin-bottom:5px;">837</div>
        <div style="font-size:12px; color:#8b92a8; letter-spacing:1px;">TOTAL VERSIONS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align:center; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px;">
        <div style="font-size:28px; color:#5f6bff; font-weight:700; margin-bottom:5px;">12.4K</div>
        <div style="font-size:12px; color:#8b92a8; letter-spacing:1px;">STREAMS TODAY</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align:center; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px;">
        <div style="font-size:28px; color:#FBC02D; font-weight:700; margin-bottom:5px;">432</div>
        <div style="font-size:12px; color:#8b92a8; letter-spacing:1px;">CONTRIBUTORS</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="text-align:center; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px;">
        <div style="font-size:28px; color:#66BB6A; font-weight:700; margin-bottom:5px;">14</div>
        <div style="font-size:12px; color:#8b92a8; letter-spacing:1px;">DAYS ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)

# Top versions leaderboard
st.markdown("<h2 style='margin-top:50px; text-align:center;'>🏆 Top Community Versions</h2>", unsafe_allow_html=True)

for i, version in enumerate(versions[:5]):
    highlight = "border: 2px solid rgba(76, 175, 80, 0.4);" if version['id'] == current['id'] else ""
    st.markdown(f"""
    <div class="track-card" style="padding:20px; margin:10px auto; max-width:700px; {highlight}">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:15px;">
                <div style="font-size:24px; color:#4CAF50; font-weight:700; min-width:40px;">#{version['rank']}</div>
                <div>
                    <div style="font-size:16px; color:#ffffff; font-weight:600;">{version['contributor']}</div>
                    <div style="font-size:12px; color:#8b92a8; margin-top:3px;">
                        Lyrics {version['features']['lyrics']} • Groove {version['features']['groove']} • {version['features']['spatialize'].title()}
                    </div>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="color:#FDD835; font-weight:600;">{version['votes']} votes</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:60px; padding:30px; background:rgba(255,255,255,0.02); border-radius:12px;">
  <div style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif; margin-bottom:10px; font-weight:600;">
    ⌨️ KEYBOARD SHORTCUTS
  </div>
  <div style="display:flex; justify-content:center; gap:20px; color:#6b7280; font-size:12px; font-family:'Inter', sans-serif;">
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">Space</kbd> Play/Pause</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">↑↓</kbd> Volume ±10%</div>
  </div>
  
  <div style="margin-top:30px; padding-top:20px; border-top:1px solid rgba(255,255,255,0.05);">
    <div style="color:#6b7280; font-size:11px; font-family:'Inter', sans-serif; line-height:1.6;">
      Each time you play, a version is selected based on community rankings.<br>
      Higher ranked versions have a greater probability of being played.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)