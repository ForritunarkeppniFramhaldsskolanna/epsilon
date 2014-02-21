
<p>Pascal-þríhyrningurinn er óendanlega stór þríhyrningur af heiltölum, skilgreindur þannig að efst í þríhyrningnum er talan 1, og er talan 1 svo í fyrsta og síðasta dálki hverrar raðar. Tölur annarstaðar í þríhyrningnum eru fengnar með því að leggja saman tölurnar tvær fyrir ofan hana. Fyrstu sjö raðirnar í þríhyrningnum líta þá svona út:</p>

<table class="pascal">
    <tr><td></td><td></td><td></td><td></td><td></td><td></td><td class="odd">1</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td></td><td></td><td></td><td></td><td></td><td class="odd">1</td><td></td><td class="odd">1</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td></td><td></td><td></td><td></td><td class="odd">1</td><td></td><td>2</td><td></td><td class="odd">1</td><td></td><td></td><td></td><td></td></tr>
    <tr><td></td><td></td><td></td><td class="odd">1</td><td></td><td class="odd">3</td><td></td><td class="odd">3</td><td></td><td class="odd">1</td><td></td><td></td><td></td></tr>
    <tr><td></td><td></td><td class="odd">1</td><td></td><td>4</td><td></td><td>6</td><td></td><td>4</td><td></td><td class="odd">1</td><td></td><td></td></tr>
    <tr><td></td><td class="odd">1</td><td></td><td class="odd">5</td><td></td><td>10</td><td></td><td>10</td><td></td><td class="odd">5</td><td></td><td class="odd">1</td><td></td></tr>
    <tr><td class="odd">1</td><td></td><td>6</td><td></td><td class="odd">15</td><td></td><td>20</td><td></td><td class="odd">15</td><td></td><td>6</td><td></td><td class="odd">1</td></tr>
</table>

<p>Ef við litum reitina sem innihalda oddatölur svarta, og reitina sem innihalda sléttar tölur hvíta, þá fáum við mynstur. Þetta mynstur heitir Sierpinski þríhyrningurinn, og er svokallaður &ldquo;fractal&rdquo;.</p>

<h2>Inntak</h2>

<p>Inntakið inniheldur eina heiltölu <tt>1 &leq; n &leq; 100</tt>.</p>

<h2>Úttak</h2>

<p>Skrifa á út fyrstu <tt>n</tt> raðirnar í Sierpinski þríhyrningnum, þar sem svartur dálkur er táknaður með &lsquo;<tt>#</tt>&rsquo;, og hvítur dálkur er táknaður með &lsquo;<tt>.</tt>&rsquo;. Athuga skal að þríhyrningurinn á að halla til vinstri.</p>

