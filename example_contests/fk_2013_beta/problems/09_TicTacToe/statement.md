
<p>Í leiknum Tic-Tac-Toe skiptast leikmenn á að setja táknið sitt í reiti á fylki af stærð <tt>3 &times; 3</tt>. Fyrri leikmaðurinn notar táknað <tt>X</tt>, en seinni leikmaðurinn notar táknið <tt>O</tt>. Leikmaður vinnur þegar hann hefur fyllt heila röð, dálk, eða aðra hvora skálínuna með tákninu sínu. Til dæmis hefur leikmaður með táknið <tt>O</tt> unnið þennan leik:</p>

<table class="ttt">
<tr>
    <td class="bb br"><tt>X</tt></td>
    <td class="bb br bl"><tt>X</tt></td>
    <td class="bb bl"></td>
</tr>
<tr>
    <td class="bt br bb"><tt>O</tt></td>
    <td class="bt bb br bl"><tt>O</tt></td>
    <td class="bt bb bl"><tt>O</tt></td>
</tr>
<tr>
    <td class="bt br"><tt>X</tt></td>
    <td class="bt bl br"></td>
    <td class="bt bl"></td>
</tr>
</table>

<p>Aftur á móti hefur enginn enn unnið þennan leik:</p>

<table class="ttt">
<tr>
    <td class="bb br"><tt>X</tt></td>
    <td class="bb br bl"></td>
    <td class="bb bl"><tt>X</tt></td>
</tr>
<tr>
    <td class="bt br bb"><tt>X</tt></td>
    <td class="bt bb br bl"><tt>O</tt></td>
    <td class="bt bb bl"><tt>X</tt></td>
</tr>
<tr>
    <td class="bt br"><tt>O</tt></td>
    <td class="bt bl br"><tt>O</tt></td>
    <td class="bt bl"></td>
</tr>
</table>

<p>Líka er hægt að spila Tic-Tac-Toe á stærra borði, eða á fylki af stærð <tt>n &times; n</tt>, þar sem <tt>n &geq; 3</tt>. Þá vinnur leikmaður ef hann hefur fyllt einhverja röð, einhvern dálk, eða aðra hvora af skálínunum með tákninu sínu.</p>

<p>Skrifið forrit sem les inn heiltöluna <tt>n</tt>, og svo <tt>n &times; n</tt> fylki með táknunum <tt>X</tt> og <tt>O</tt>. Forritið á svo að skrifa út hvort leikmaður <tt>X</tt> sé búinn að vinna, leikmaður <tt>O</tt> sé búinn að vinna, eða enginn sé enn búinn að vinna. Ef sú staða kemur upp að báðir leikmenn hafa unnið á að skrifa út villumeldingu.</p>

<h2>Inntak</h2>

<p>Á fyrstu línu er heiltalan <tt>1 &leq; T &leq; 100</tt>, sem táknar fjölda prófunartilvika sem fylgja. Hvert prófunartilvik byrjar á einni línu með heiltölunni <tt>3 &leq; n &leq; 100</tt>. Næstu <tt>n</tt> línur innihalda hver <tt>n</tt> stafi, þar sem stafirnir eru <tt>X</tt>, <tt>O</tt>, og <tt>.</tt> (punktur). Punktur táknar auðan reit.</p>

<h2>Úttak</h2>

<p>Fyrir hvert prófunartilvik á að skrifa út eina línu sem inniheldur &ldquo;<tt>X won</tt>&rdquo; ef leikmaður <tt>X</tt> vann, &ldquo;<tt>O won</tt>&rdquo; ef leikmaður <tt>O</tt> vann, &ldquo;<tt>Neither won</tt>&rdquo; ef enginn er enn búinn að vinna, eða &ldquo;<tt>Error</tt>&rdquo; ef báðir eru búnir að vinna.</p>

