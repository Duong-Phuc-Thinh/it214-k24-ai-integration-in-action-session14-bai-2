# Dong bo trang thai don hang lac loi

## Mo ta
Bai tap giai quyet bai toan dong bo trang thai don hang giua Order Service va Payment Service, xu ly truong hop mat ket noi mang hoac timeout.

## Chuc nang
- Xu ly su kien phan hoi thanh toan (SUCCESS, REJECTED, FAILED).
- Co che Scheduled Job (Background Task) de quet cac don hang PENDING qua han (vi du qua 5 phut) va chuyen sang FAILED.
- Mo phong State Machine cua don hang.

## Huong dan chay
```bash
python main.py
```