
<p>Gömul japönsk aðferð til að reikna <tt>&radic;<span style="text-decoration:overline">n</span></tt> (kvaðratrót af <tt>n</tt>) er eftirfarandi:</p>


<blockquote>
Búðu til breyturnar <tt>a</tt> og <tt>b</tt>.<br />
Breytan <tt>a</tt> tekur gildið <tt>5 &times; n</tt> og breytan <tt>b</tt> gildið <tt>5</tt>.<br />
<br />
Eftirfarandi skref er hægt að gera oft til að fá meiri nákvæmni (þetta á að gera <tt>i</tt> sinnum, sjá lýsingu að neðan):

<blockquote>
    ef <tt>a &geq; b</tt>:
    <blockquote>
        <tt>a</tt> tekur gildið <tt>a - b</tt><br />
        <tt>b</tt> tekur gildið <tt>b + 10</tt>
    </blockquote>
    annars:
    <blockquote>
        bæta tveimur núllum fyrir aftan <tt>a</tt><br />
        bæta einu núlli á milli næstsíðasta og síðasta tölustafsins í <tt>b</tt>
    </blockquote>
</blockquote>

Breytan <tt>b</tt> inniheldur svo svarið.

</blockquote>

<p>Þú átt að lesa inn tölurnar <tt>n</tt> og <tt>i</tt>. Notaðu svo aðferðina til að reikna <tt>&radic;<span style="text-decoration:overline">n</span></tt>. Framkvæmdu milliskrefið <tt>i</tt> sinnum og skrifaðu svo út lokagildi <tt>b</tt>.</p>

<h2>Inntak</h2>

<p>Á fyrstu línu er heiltalan <tt>1 &leq; T &leq; 100</tt>, sem táknar fjölda prófunartilvika sem fylgja. Hvert prófunartilvik samanstendur af einni línu með tveimur heiltölum <tt>1 &lt; n &leq; 10000</tt> og <tt>1 &leq; i &leq; 1000</tt>, aðskildum með bili.</p>

<h2>Úttak</h2>

<p>Fyrir hvert prófunartilvik á að skrifa út eina línu sem inniheldur lokagildi <tt>b</tt>.</p>

