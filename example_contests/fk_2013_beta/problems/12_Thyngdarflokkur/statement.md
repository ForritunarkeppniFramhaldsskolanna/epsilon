
<p>Verið er að undirbúa kraftlyftingakeppni sem haldin verður á næstunni. Keppendum er skipt upp í þrjá þyngdarflokka; léttvigt, millivigt og þungavigt. Eftirfarandi sýnir hvernig keppendunum er skipt upp eftir þyngd:</p>

<table style="text-align:center;width:220px;margin:0 auto;border-collapse:collapse">
    <tr>
        <td style="border-bottom:1px solid black">Flokkur</td>
        <td style="border-bottom:1px solid black">Þyngd (kg)</td>
    </tr>
    <tr>
        <td>Léttvigt</td>
        <td><tt>&lt; 60</tt></td>
    </tr>
    <tr>
        <td>Millivigt</td>
        <td><tt>&geq; 60</tt> og <tt>&leq; 90</tt></td>
    </tr>
    <tr>
        <td>Þungavigt</td>
        <td><tt>&gt; 90</tt></td>
    </tr>
</table>

<p>Skrifið forrit sem les inn nöfn og þyngd keppenda, og skrifar út hvaða flokki hver keppandi tilheyrir.</p>

<h2>Inntak</h2>

<p>Á fyrstu línu er heiltalan <tt>1 &leq; T &leq; 100</tt>, sem táknar fjölda prófunartilvika sem fylgja. Hvert prófunartilvik samanstendur af tveimur línum. Fyrri línan inniheldur nafn keppandans, og seinni línan inniheldur kommutölu sem táknar þyngd keppandans í kílógrömmum.</p>

<h2>Úttak</h2>

<p>Fyrir hvert prófunartilvik á að skrifa út eina línu. Ef keppandinn tilheyrir léttvigt á línan að innihalda &ldquo;<i>nafn</i> <tt>competes in lightweight</tt>&rdquo;. Ef keppandinn tilheyrir millivigt á línan að innihalda &ldquo;<i>nafn</i> <tt>competes in middleweight</tt>&rdquo;. Ef keppandinn tilheyrir þungavigt á línan að innihalda &ldquo;<i>nafn</i> <tt>competes in heavyweight</tt>&rdquo;.</p>

