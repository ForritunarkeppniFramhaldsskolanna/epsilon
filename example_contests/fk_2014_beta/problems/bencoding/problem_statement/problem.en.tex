
<img src="assets/bittorrent.jpg" alt="bittorrent" class="img-polaroid" style="float:right;width:30%;margin:6px;" />

BitTorrent er mikið notaður <abbr title="file transfer
protocol">skráardeilingarstaðall</abbr>. Hann er keyrður í <abbr title="peer to
peer">jafningjaneti</abbr> og samanstendur af <abbr
title="client">biðlurum</abbr> og svokölluðum <abbr
title="tracker">sporrekjendum</abbr>. Sporrekjandinn heldur utan um hvaða
biðlarar eru að deila hvaða skrám, og nýjir biðlarar hafa því samskipti við
sporrekjandann til að fá upplýsingar um þá sem eru að deila skrá sem biðlarinn
vill ná í.

Þessi samskipti fara fram á formi sem kallað er Bencoding. Þetta form getur
táknað heiltölur, strengi, lista og svokallaðar <abbr
title="dictionary">orðabækur</abbr>, og gerir það á eftirfarandi hátt:

- Heiltala $x$ er geymd sem **i**$x$**e**. T.d. er $123$ geymd sem **i123e**.
- Strengur $s$ af lengd $n$ er geymdur sem $n$**:**$s$. T.d. er strengurinn
  "banani" geymdur sem **6:banani**.
- Listi sem inniheldur stökin $a_1, a_2, \ldots, a_n$ er geymdur sem
  **l**$A_1$$A_2$$\ldots$$A_n$**e**, þar sem $A_i$ er Bencoding formið á
  stakinu $a_i$. T.d. er listi sem inniheldur fyrst heiltöluna 10, svo
  strenginn "hello", og að lokum strenginn "world", geymdur sem
  **li10e5:hello5:worlde**.
- Orðabók sem hefur lykilinn $k_1$ paraðann við gildið $v_1$, $\ldots$,
  lykilinn $k_n$ paraðann við gildið $v_n$, er geymdur sem
  **d**$K_1$$V_1$$\ldots$$K_n$$V_n$**e**, þar sem $K_i$ og $V_i$ eru Bencoding
  formin á $k_i$ og $v_i$. T.d. er orðabók sem hefur lykilinn "banani" paraðann
  við gildið $123$, og lykilinn "X" paraðann við gildið "Leet", geymd sem
  **d6:bananii123e1:X4:Leete**. Athugið að röð lyklanna skiptir ekki máli, og
  er líka hægt að geyma þessa orðabók sem **d1:X4:Leet6:bananii123ee**.

Athugið að listar geta innihaldið aðra lista og orðabækur, og orðabækur geta
innihaldið lista og aðrar orðabækur sem gildi. Lyklar í orðabók eru strengir,
og engir tveir þeirra eru eins.

Í þessu verkefni eigið þið að umbreyta gögnum sem geymd eru á Bencoding formi
yfir á eftirfarandi form, sem auðveldara er að lesa úr:

- Heiltala $x$ er geymd sem $x$. T.d. er $123$ geymd sem **123**.
- Strengur $s$ er geymdur sem "$s$" (þ.e. $s$ umkringdur gæsalöppum). T.d. er
  strengurinn "banani" geymdur sem **"banani"**.
- Listi sem inniheldur stökin $a_1, a_2, \ldots, a_n$ er geymdur sem
  [$a_1$,$a_2$,$\ldots$,$a_n$]. T.d. er listi sem inniheldur fyrst heiltöluna
  10, svo strenginn "hello", og að lokum strenginn "world", geymdur sem
  **[10,"hello","world"]**.
- Orðabók sem hefur lykilinn $k_1$ paraðann við gildið $v_1$, $\ldots$,
  lykilinn $k_n$ paraðann við gildið $v_n$, er geymdur sem
  {$k_1$:$v_1$,$\ldots$,$k_n$:$v_n$}. T.d. er orðabók sem hefur lykilinn
  "banani" paraðann við gildið $123$, og lykilinn "X" paraðann við gildið
  "Leet", geymd sem **{"banani":123,"X":"Leet"}**. Athugið að röð lyklanna
  skiptir ekki máli, og er líka hægt að geyma þessa orðabók sem
  **{"X":"Leet","banani":123}**.

Inntakið inniheldur eina línu með gögnum á Bencoding formi. Úttakið á að
innihalda eina línu með sömu gögnum á seinna forminu.


