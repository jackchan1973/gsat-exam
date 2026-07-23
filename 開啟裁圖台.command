#!/bin/bash
# 雙擊此檔即可開啟「人機協同裁圖台」。
# 會在本機起一個小伺服器並自動開瀏覽器；用完把這個黑色視窗關掉即可停止。
cd "$(dirname "$0")/tools/裁圖台" || exit 1
PORT=8790
URL="http://localhost:${PORT}"
echo "啟動裁圖台 … 瀏覽器沒自動打開的話，手動開： ${URL}"
# 「存到交件匣」需要 Chrome，優先用 Chrome 開；沒有 Chrome 才退回預設瀏覽器
( sleep 1; open -a "Google Chrome" "${URL}" 2>/dev/null || open "${URL}" ) &
python3 -m http.server "${PORT}"
