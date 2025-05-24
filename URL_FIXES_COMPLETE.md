# URL KORREKTUREN - St. Pölten Musikschule

## ❌ ALTE FALSCHE URLs:
- `/blog/manage/` → existiert nicht
- `/gallery/admin/` → existiert nicht 
- `/team/controlling/students/` → existiert nicht
- `/events/manage/` → existiert nicht

## ✅ NEUE KORREKTE URLs:
- `/blogedit/summary/` → Blog Management (show_blogs_editing)
- `/galerie/admin/` → Gallery Admin (gallery_admin)
- `/team/controlling/students` → Student Management (get_controlling_students)
- `/team/events` → Event Management (event_managing_view)

## 🔧 GEÄNDERTE DATEIEN:
- `static/js/navigation/mks_overlay_menu.js`
  - handleStatCardClick() Funktion
  - getUrlByName() Mapping

## ✅ BESTÄTIGT FUNKTIONIERENDE URLs:
1. **Blog Management:** `/blogedit/summary/`
2. **Gallery Admin:** `/galerie/admin/`  
3. **Student Management:** `/team/controlling/students`
4. **Event Management:** `/team/events`

## 🎯 WICHTIG:
Die Statistik-Karten sind deaktiviert (`disabled-stat`), aber die URLs sind trotzdem korrigiert falls sie in der Zukunft wieder aktiviert werden.

## ✅ STATUS: URLs KORRIGIERT UND FUNKTIONAL
