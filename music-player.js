// ============== 背景音乐控制（两首循环 + 跨页面连续） ==============
(function() {
    var audio1 = document.getElementById('bgMusic1');
    var audio2 = document.getElementById('bgMusic2');
    var musicDisc = document.getElementById('musicDisc');
    var musicToggle = document.getElementById('musicToggle');
    var musicPlayer = document.getElementById('musicPlayer');
    if (!audio1 || !audio2 || !musicPlayer) return;
    var STORAGE_KEY = 'stardew_bg_music2';
    var playlist = [audio1, audio2];
    var currentIdx = 0;
    var musicPlaying = false;

    function saveMusicState() {
        var state = {
            currentTime: playlist[currentIdx].currentTime,
            playing: musicPlaying,
            trackIndex: currentIdx
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    function switchTrack(idx) {
        playlist[currentIdx].pause();
        playlist[currentIdx].currentTime = 0;
        currentIdx = idx % playlist.length;
    }

    function startMusic() {
        if (musicPlaying) return;
        playlist[currentIdx].volume = 0.3;
        playlist[currentIdx].play().then(function() {
            musicDisc.classList.add('playing');
            musicToggle.textContent = '\u{1F50A}';
            musicPlaying = true;
        }).catch(function() {});
    }

    function stopMusic() {
        playlist[currentIdx].pause();
        musicDisc.classList.remove('playing');
        musicToggle.textContent = '\u{1F507}';
        musicPlaying = false;
    }

    // 播放完一首自动切下一首
    playlist.forEach(function(audio) {
        audio.addEventListener('ended', function() {
            if (musicPlaying) {
                switchTrack(currentIdx + 1);
                startMusic();
            }
        });
    });

    // 定时保存状态，防止刷新时丢失
    setInterval(function() {
        if (musicPlaying) {
            saveMusicState();
        }
    }, 1000);

    musicPlayer.addEventListener('click', function() {
        if (musicPlaying) {
            stopMusic();
        } else {
            startMusic();
        }
    });

    // 页面加载时：恢复上次播放位置，但不自动播放
    function restoreMusicState() {
        var saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            try {
                var state = JSON.parse(saved);
                currentIdx = state.trackIndex || 0;
                if (currentIdx >= playlist.length) currentIdx = 0;
                playlist[currentIdx].currentTime = state.currentTime || 0;
            } catch(e) {}
        }
        // 确保唱片不旋转、音乐不播放
        musicDisc.classList.remove('playing');
        musicToggle.textContent = '\u{1F507}';
        // 重置保存的播放状态为 false，防止跨页面自动播放
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
            currentTime: playlist[currentIdx].currentTime,
            playing: false,
            trackIndex: currentIdx
        }));
    }

    document.addEventListener('DOMContentLoaded', restoreMusicState);

    window.addEventListener('beforeunload', saveMusicState);
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') saveMusicState();
    });
})();