
<p>Forritunarmálið Befunge er sniðugt, en óhefðbundið forritunarmál. Hér er dæmi um Befunge forrit sem skrifar strenginn &ldquo;<tt>Hello World</tt>&rdquo; óendanlega oft út:</p>

<table style="margin:0 auto;border: 1px solid black;padding:2px;">
<tr>
    <td><tt>&gt;"dlroW olleH"v</tt></td>
</tr>
<tr>
    <td><tt>^ ,,,,,,,,,,, &lt;</tt></td>
</tr>
</table>

<p>Þegar Befunge kóði er keyrður er notaður svokallaður skipanabendir, eða bara bendir, sem bendir á hvar í forritinu við erum. Í byrjun keyrslunnar bendir bendirinn á fyrsta stafinn í efstu línunni, sem í þessu tilfelli er stafurinn &lsquo;<tt>&gt;</tt>&rsquo;. Stafurinn &lsquo;<tt>&gt;</tt>&rsquo; segir bendinum að breyta um stefnu og halda áfram að lesa skipanir í áttina til hægri. Þess vegna mun bendirinn halda núna áfram til hægri og lesa næst stafinn &lsquo;<tt>"</tt>&rsquo;, svo stafinn &lsquo;<tt>d</tt>&rsquo;, og svo framvegis. Það sem forritið gerir núna er að setja stafina í strengnum &ldquo;<tt>Hello World</tt>&rdquo; í svokallaðan stafla, en það þarf ekki að skilja þennan hluta fyrir þetta dæmi. Loks kemur bendirinn að stafnum &lsquo;<tt>v</tt>&rsquo;, en hann segir bendinum að breyta um stefnu og halda áfram að lesa skipanir í áttina niður. Þá kemur bendirinn að stafnum &lsquo;<tt>&lt;</tt>&rsquo;, sem segir bendinum að breyta um stefnu og halda áfram að lesa skipanir til vinstri. Næst kemur bendirinn að auðu bili, en autt bil hefur enga merkingu í Befunge, og því heldur bendirinn bara áfram í sömu átt. Þá kemur bendirinn að runu af kommum, og lætur hver komma forritið taka efsta stafinn af staflanum og skrifa hann út á skjáinn, en það þarf ekki að skilja þennan hluta fyrir þetta dæmi. Loks kemur hann að stafnum &lsquo;<tt>^</tt>&rsquo; (þetta er stafurinn sem oft er notaður til að tákna veldi, og er kallaður hattur), sem segir bendinum að breyta um stefnu og lesa skipanir í áttina upp. Þá kemur bendirinn aftur á þann stað sem hann byrjaði á, snýr sér svo til hægri, og framkvæmir þá sömu röð af skipunum aftur. Þetta gerir forritið svo óendanlega oft, og er þetta kölluð óendanleg lykkja.</p>

<p>Tökum svo annað, mjög svipað dæmi um Befunge kóða:</p>

<table style="margin:0 auto;border: 1px solid black;padding:2px;">
<tr>
    <td><tt>&gt;"dlroW olleH"v</tt></td>
</tr>
<tr>
    <td><tt>^@,,,,,,,,,,, &lt;</tt></td>
</tr>
</table>

<p>Þetta Befunge forrit mun framkvæma sömu röð af skipunum og forritið að ofan, alveg þangað til að það kemur að stafnum &lsquo;<tt>@</tt>&rsquo;, en stafurinn &lsquo;<tt>@</tt>&rsquo; segir Befunge forritinu að hætta. Þess vegna mun þetta forrit skrifa út &ldquo;<tt>Hello World</tt>&rdquo; einu sinni, og hætta svo. Þetta forrit inniheldur því ekki óendanlega lykkju.</p>

<p>Í þessu dæmi ætlum við að skoða smækkaða útgáfu af forritunarmálinu Befunge, en aðeins skipanirnar &lsquo;<tt>&gt;</tt>&rsquo;, &lsquo;<tt>v</tt>&rsquo;, &lsquo;<tt>&lt;</tt>&rsquo;, &lsquo;<tt>^</tt>&rsquo; og &lsquo;<tt>@</tt>&rsquo; eru leyfðar, og auk þess eru auð bil og línubil leyfð. Til að forðast vandræði með inntak skulum við láta punkt (&lsquo;<tt>.</tt>&rsquo;) tákna autt bil. Skrifið forrit sem les inn svona Befunge kóða, og ákvarðar hvort forritið innihaldi óendanlega lykkju, eða hætti með venjulegum hætti. Gera má ráð fyrir að bendirinn fari aldrei út fyrir textann í forritinu. Líka má gera ráð fyrir því að línurnar í forritskóðanum séu allar jafn langar.</p>

<h2>Inntak</h2>

<p>Á fyrstu línu er heiltalan <tt>1 &leq; T &leq; 100</tt>, sem táknar fjölda prófunartilvika sem fylgja. Hvert prófunartilvik samanstendur af nokkrum línum með forritskóða úr smækkaðri útgáfu af Befunge eins og skilgreint er að ofan. Endirinn á kóðanum er táknaður með einni línu sem inniheldur aðeins stafinn &lsquo;<tt>#</tt>&rsquo;, en það er ekki tekið með sem hluti af kóðanum.</p>

<h2>Úttak</h2>

<p>Fyrir hvert prófunartilvik á að skrifa út eina línu sem inniheldur strenginn &ldquo;<tt>Terminates</tt>&rdquo; ef forritið hættir á venjulegan hátt, en strenginn &ldquo;<tt>Infinite loop</tt>&rdquo; ef forritið inniheldur óendanlega lykkju.</p>

