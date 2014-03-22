
Þegar tölva tengist internetinu, þá er henni úthlutað IP tölu. Hver tölva fær
mismunandi IP tölu, og er því hægt að nota IP töluna til að hafa samband við
samsvarandi tölvu. Í útgáfu 4 af IP staðlinum (IPv4) er í mesta lagi hægt að hafa
$2^{32}$ mismunandi IP tölur. Á síðustu árum hefur fjöldi nettengdra tölva
aukist verulega, og stefnir því fljótlega í að allar IP tölur í útgáfu 4 af
staðlinum klárist. Þetta varð til þess að í útgáfu 6 af IP staðlinum (IPv6) var bætt
við mikið af IP tölum, en þar eru $2^{64}$ mismunandi IP tölur.

Báðar útgáfurnar af staðlinum eru í notkun í dag, og gerir það
hugbúnaðarframleiðendum erfitt fyrir. Ykkar verkefni er að skrifa forrit sem
les inn streng, og segja hvort strengurinn tákni IPv4 tölu eða IPv6 tölu.

IPv4 tala er á forminu <tt>X.X.X.X</tt> þar sem <tt>X</tt> er heiltala á bilinu
$0$ upp í $255$. Dæmi um IPv4 tölu er <tt>192.168.0.32</tt>. Athugið að
tölurnar mega ekki innihalda óþarfa $0$ í byrjun.

IPv6 tala er á forminu <tt>Y:Y:Y:Y:Y:Y:Y:Y</tt> þar sem <tt>Y</tt> er strengur
af lengd 4 sem inniheldur tölustafi eða stafina <tt>a,b,c,d,e,f</tt>. Dæmi um
IPv6 tölu er <tt>2001:0db8:85a3:e042:0000:8a2e:03ff:abcd</tt>.

Inntak inniheldur eina línu. Úttak er ein lína sem er <tt>IPv4</tt> ef inntakið
táknar IPv4 tölu, <tt>IPv6</tt> ef inntakið táknar IPv6 tölu, en <tt>Error</tt>
ef inntakið táknar hvorugt.

