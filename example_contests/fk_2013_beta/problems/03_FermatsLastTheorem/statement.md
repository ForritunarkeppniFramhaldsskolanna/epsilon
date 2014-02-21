Pierre de Fermat er franskur stærðfræðingur sem uppi var á 17. öld. Þekktastur er hann fyrir eftirfarandi tilgátu:

> Ekki eru til neinar pósitífar heiltölur `a`, `b` og `c` sem
> uppfylla jöfnuna <code>a<sup>n</sup> + b<sup>n</sup> = c<sup>n</sup></code> þegar `n`
> er heiltala stærri en `2`.

Fermat skrifaði þessa tilgátu í spássíu bókar sem hann var að lesa, og sagðist hafa sönnun fyrir tilgátunni, en hún væri of löng til að komast fyrir á spássíunni. Margir stærðfræðingar reyndu að sanna tilgátuna eftir þetta, en það var ekki fyrr en rúmlega 300 árum síðar að breski stærðfræðingurinn Andrew Wiles kom loksins með sönnun. Tilgátan reyndist því vera sönn, og er nú kölluð &ldquo;síðasta setning Fermats.&rdquo;

## Inntak

Á fyrstu línu er heiltalan <code>1 &leq; T &leq; 100</code>, sem táknar fjölda prófunartilvika sem fylgja. Hvert prófunartilvik samanstendur af einni línu með heiltölunni <code>2 < n < 10<sup>100</sup></code>.

## Úttak

Fyrir hvert prófunartilvik á að skrifa út allar pósitífar heiltölur `a`, `b` og `c` sem uppfylla jöfnuna <code>a<sup>n</sup> + b<sup>n</sup> = c<sup>n</sup></code>. Skrifa á út eina lausn á línu á forminu &ldquo;<code>a b c</code>&rdquo;. Ekki skiptir máli í hvaða röð lausnirnar eru skrifaðar út. Ef það eru ekki neinar lausnir, þá á að skrifa út eina línu á forminu &ldquo;<code>no solutions when n = <i>n</i></code>&rdquo;.

