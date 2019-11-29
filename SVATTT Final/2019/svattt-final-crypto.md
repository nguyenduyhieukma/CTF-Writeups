# Gợi ý giải 2 thử thách Mật mã tại Vòng Chung khảo Sinh viên với An toàn thông tin 2019

## ratio
### Đề bài
Cho 2 đường thằng `l1` và `l2` giao nhau tại `O`. Lấy ngẫu nhiên `P1` thuộc `l1`, `P2` thuộc `l2` và  `R` thuộc đoạn`P1-P2` sao cho `R-P1/R-P2 = O-P1/O-P2` (`r1/r2 = d1/d2` như hình vẽ). Các tọa độ điểm và hệ số thuộc trường hữu hạn `Fp` có `p = 0x1ffff` dài 17 bit. Biết `l1`, `l2`, `P2`, và FLAG mã hóa bằng `R`, tìm FLAG.

![](ratio.png)

### Lời giải
Dễ thấy, ta có thể vét cạn `P1` (khoảng `2^17` khả năng), tính `R` từ `P1`, `P2` và dùng `R` để giải mã FLAG cho đến khi việc giải mã thành công (FLAG chỉ gồm các ký tự in được và tuân theo định dạng cho trước).

Tuy nhiên, thông tin về `P2` không được xác thực (không có MAC đi kèm) nên nhiều khả năng sẽ bị chỉnh sửa khi đi qua proxy của các đội chơi. Ngoài ra, việc vét cạn đồng thời `P1` và `P2` là không khả
thi (vì có đến khoảng `2^34` trường hợp cần vét cạn trong thời gian mội vòng thi).

Để giải quyết trọn vẹn thử thách, thí sinh cần tận dụng tính chất `OR` là một tia phân giác góc `O` (do `r1/r2 = d1/d2`) để vét cạn `R` trên 2 đường phân giác (2 đường nét đứt như hình vẽ, khoảng 2^18 trường hợp) và giải mã FLAG bất kể việc thông tin về `P2` có thể đã bị chỉnh sửa.

## tangent
### Đề bài
Biết 3 tiếp tuyến của một parabol, tìm parabol đó.

### Lời giải
Giả sử parabol cần tìm có phương trình `y = a*x^2 + b*x + c`, và 3 tiếp tuyến đã biết là `y = D1*x + E1`, `y = D2*x + E2`, `y = D3*x +E3` lần lượt tiếp xúc với parabol tại 3 điểm có hoành độ lần lượt `x1`, `x2`, `x3`. Ta có hệ 6 phương trình 6 ẩn `a`, `b`, `c`, `x1`, `x2`, `x3` như sau:
- `a*x1^2 + b*x1 + c = D1*x1 + E1` (tung độ bằng nhau)
- `2*a*x1 + b = D1` (hệ số góc bằng nhau)
- `a*x2^2 + b*x2 + c = D2*x2 + E2`
- `2*a*x2 + b = D2`
- `a*x3^2 + b*x3 + c = D3*x3 + E3`
- `2*a*x3 + b = D3`

Để giải hệ trên, ta có thể tham khảo qua về  [Gröbner basis](`https://en.wikipedia.org/wiki/Gr%C3%B6bner_basis`), một phương pháp dùng đơn giản tập sinh của một ideal trong một vành đa thức.

```python
R.<a,b,c,x1,x2,x3> = Fp[]
I = R.ideal([
    a*x1^2 + b*x1 + c - D1*x1 - E1,
    2*a*x1 + b        - D1,
    a*x2^2 + b*x2 + c - D2*x2 - E2,
    2*a*x2 + b        - D2,
    a*x3^2 + b*x3 + c - D3*x3 - E3,
    2*a*x3 + b        - D3,
])
for eq in I.groebner_basis():
    print eq
```

    a + 13519595993756982943911425953069386889357602195341201210182139905440532547071
    b + 88352237532242254333616968216116575011194983617996512322023265993686331256870
    c + 38395428252004848695602380761147531916109099144945995355373078658526440611142
    x1 + 110146487338087829886990209788650092915843610697235244410622464563556998302234
    x2 + 109421061134853988937604618194787426340784567191155257329900481408591903114639
    x3 + 90552219286410288558694746889356764496292731478815082483446420669588193751758

```python
decrypt_flag(secret=p-38395428252004848695602380761147531916109099144945995355373078658526440611142)
```

    SVATTT2019{__1_w4lk_th3_l1n3_____________________________}
