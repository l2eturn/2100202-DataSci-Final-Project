#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  record.sh  —  อัดหน้าจอโปรเจกต์ Data Science
#  ใช้งาน:  bash record.sh
# ─────────────────────────────────────────────

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HTML_FILE="$PROJECT_DIR/index.html"
OUTPUT_DIR="$PROJECT_DIR/outputs"
RECORDING_DIR="$HOME/Videos"

# สีสำหรับ terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_banner() {
  echo ""
  echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║   🎬  Data Science Project — Screen Recorder  ║${NC}"
  echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
  echo ""
}

check_deps() {
  local missing=()
  for cmd in kazam xdg-open; do
    if ! command -v "$cmd" &>/dev/null; then
      missing+=("$cmd")
    fi
  done

  if [ ${#missing[@]} -ne 0 ]; then
    echo -e "${RED}❌ ไม่พบโปรแกรม: ${missing[*]}${NC}"
    echo "   ติดตั้งด้วย: sudo apt install ${missing[*]}"
    exit 1
  fi
}

choose_mode() {
  echo -e "${YELLOW}เลือกโหมดการอัด:${NC}"
  echo "  1) อัดเต็มหน้าจอ (Fullscreen) — แนะนำ"
  echo "  2) อัดเฉพาะหน้าต่าง (Window)  — เลือกหน้าต่างที่ต้องการ"
  echo "  3) เปิดแค่ Kazam (ตั้งค่าเอง)"
  echo ""
  read -rp "พิมพ์ตัวเลข [1-3]: " MODE
  MODE="${MODE:-1}"
}

open_project() {
  if [ -f "$HTML_FILE" ]; then
    echo -e "${GREEN}🌐 เปิดไฟล์โปรเจกต์ในเบราว์เซอร์...${NC}"
    xdg-open "$HTML_FILE" &
    sleep 2
  else
    echo -e "${YELLOW}⚠️  ไม่พบ index.html — จะเปิดโฟลเดอร์ outputs แทน${NC}"
    xdg-open "$OUTPUT_DIR" &
    sleep 1
  fi
}

launch_kazam() {
  mkdir -p "$RECORDING_DIR"

  echo ""
  echo -e "${GREEN}🎬 เปิด Kazam...${NC}"
  echo ""
  echo -e "${YELLOW}วิธีใช้ Kazam:${NC}"
  echo "  ① กด  Capture  (ปุ่มสีแดง) เพื่อเริ่มอัด"
  echo "  ② กด  Finish   เพื่อหยุดอัด"
  echo "  ③ ไฟล์จะถูกบันทึกไปที่: ${RECORDING_DIR}/"
  echo ""
  echo -e "${BLUE}ℹ️  ไฟล์วิดีโอจะอยู่ใน: ~/Videos/${NC}"
  echo ""

  case "$MODE" in
    1) kazam --fullscreen &;;
    2) kazam --window &;;
    3) kazam &;;
    *) kazam &;;
  esac

  KAZAM_PID=$!
  echo -e "${GREEN}✅ Kazam เปิดแล้ว (PID: $KAZAM_PID)${NC}"
}

show_tips() {
  echo ""
  echo -e "${BLUE}──────────────────────────────────────────────${NC}"
  echo -e "${YELLOW}💡 เคล็ดลับการนำเสนอ:${NC}"
  echo "  • เปิด index.html แล้ว scroll ช้า ๆ ให้คนดูตาม"
  echo "  • อธิบายแต่ละ Chart ก่อน scroll ต่อ"
  echo "  • เปิด outputs/ แล้วซูม chart ที่น่าสนใจ"
  echo "  • พูดถึง Q1-Q4 ตามลำดับ"
  echo ""
  echo -e "${BLUE}📁 Shortcut ไฟล์สำคัญ:${NC}"
  echo "  HTML:    $HTML_FILE"
  echo "  Charts:  $OUTPUT_DIR/"
  echo "  Videos:  $RECORDING_DIR/"
  echo -e "${BLUE}──────────────────────────────────────────────${NC}"
  echo ""
}

# ── Main ──
print_banner
check_deps
choose_mode
open_project
show_tips
launch_kazam
