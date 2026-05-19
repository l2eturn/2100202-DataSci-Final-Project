#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  install_ffmpeg_recorder.sh
#  ติดตั้ง ffmpeg แล้วอัดหน้าจอแบบ command-line
#  ใช้งาน:  bash install_ffmpeg_recorder.sh
# ─────────────────────────────────────────────

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

OUTPUT_DIR="$HOME/Videos"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE="$OUTPUT_DIR/datasci_project_${TIMESTAMP}.mp4"

SCREEN_RES="1920x1080"   # ความละเอียดหน้าจอ (เปลี่ยนได้)
FPS=30                   # เฟรมต่อวินาที
DISPLAY_NUM=":1"         # display ที่ใช้

install_ffmpeg() {
  if command -v ffmpeg &>/dev/null; then
    echo -e "${GREEN}✅ ffmpeg ติดตั้งแล้ว: $(ffmpeg -version 2>&1 | head -1)${NC}"
  else
    echo -e "${YELLOW}📦 กำลังติดตั้ง ffmpeg...${NC}"
    sudo apt update -qq
    sudo apt install -y ffmpeg
    echo -e "${GREEN}✅ ติดตั้ง ffmpeg สำเร็จ${NC}"
  fi
}

choose_options() {
  echo ""
  echo -e "${YELLOW}─── ตั้งค่าการอัด ───${NC}"

  read -rp "ความละเอียด [${SCREEN_RES}]: " input_res
  SCREEN_RES="${input_res:-$SCREEN_RES}"

  read -rp "FPS [${FPS}]: " input_fps
  FPS="${input_fps:-$FPS}"

  echo ""
  echo -e "${YELLOW}เลือกเสียง:${NC}"
  echo "  1) ไม่อัดเสียง"
  echo "  2) อัดเสียงจากไมค์ (PulseAudio)"
  read -rp "เลือก [1-2]: " audio_choice
  AUDIO_CHOICE="${audio_choice:-1}"

  echo ""
  echo -e "${BLUE}📁 ไฟล์จะบันทึกที่: ${OUTPUT_FILE}${NC}"
  echo ""
}

record_screen() {
  mkdir -p "$OUTPUT_DIR"

  echo -e "${GREEN}🔴 เริ่มอัดหน้าจอ...${NC}"
  echo -e "${YELLOW}   กด  Ctrl+C  เพื่อหยุดอัด${NC}"
  echo ""

  if [ "$AUDIO_CHOICE" = "2" ]; then
    # อัดพร้อมเสียง PulseAudio
    ffmpeg \
      -f x11grab \
      -r "$FPS" \
      -s "$SCREEN_RES" \
      -i "${DISPLAY_NUM}.0+0,0" \
      -f pulse \
      -i default \
      -c:v libx264 \
      -preset ultrafast \
      -crf 23 \
      -c:a aac \
      -b:a 128k \
      -pix_fmt yuv420p \
      "$OUTPUT_FILE"
  else
    # อัดแค่หน้าจอ ไม่มีเสียง
    ffmpeg \
      -f x11grab \
      -r "$FPS" \
      -s "$SCREEN_RES" \
      -i "${DISPLAY_NUM}.0+0,0" \
      -c:v libx264 \
      -preset ultrafast \
      -crf 23 \
      -pix_fmt yuv420p \
      "$OUTPUT_FILE"
  fi
}

show_result() {
  echo ""
  if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -sh "$OUTPUT_FILE" | cut -f1)
    echo -e "${GREEN}✅ อัดเสร็จแล้ว!${NC}"
    echo -e "   ไฟล์: ${BLUE}${OUTPUT_FILE}${NC}"
    echo -e "   ขนาด: ${SIZE}"
    echo ""
    echo -e "${YELLOW}💡 เปิดดูด้วย:${NC}  xdg-open \"$OUTPUT_FILE\""
  else
    echo -e "${RED}❌ ไม่พบไฟล์วิดีโอ — การอัดอาจถูกยกเลิก${NC}"
  fi
}

# ── Main ──
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🎬  FFmpeg Screen Recorder — Setup & Record  ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""

install_ffmpeg
choose_options
record_screen
show_result
