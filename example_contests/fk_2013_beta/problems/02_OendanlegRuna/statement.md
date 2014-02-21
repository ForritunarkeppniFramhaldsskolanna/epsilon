Jón litli á von á vini sínum í heimsókn, en þeir eru búnir að skipuleggja
brjálað LAN kvöld og ætla að spila alla uppáhalds tölvuleikina sína. Jón er
búinn að bíða í allan dag og er ekkert smá spenntur. En þá hringir vinur hans
og segist því miður ekki geta komist, en hann sé orðinn fárveikur.

Það er ekkert gaman að spila þessa tölvuleiki einn, þannig Jóni fer að leiðast.
Þá fær hann allt í einu snilldar hugmynd. Hann ætlar að búa til óendanlega
stóra tölu með því að taka eitthverja litla tölu og bæta henni aftan við sig
óendanlega oft.

Til dæmis, hann velur töluna `6883`, og bætir henni óendanlega oft aftan við
sig, og fær þá óendanlega stóru töluna

<pre style="text-align:center"><code>68<span style="text-decoration:underline">83688</span>36883688368836883688368836883688368836883688368836883&hellip;</code></pre>

Hann byrjar að skrifa töluna niður á blað, en eftir að hafa skrifað í hálftíma
og fyllt tvær heilar blaðsíður ákveður hann að stoppa. Talan er svo stór! Hún
er óendanlega stór! Honum langar að skoða töluna betur, og þá sérstaklega
hvernig smá partur af henni lítur út á ákveðnum stöðum. Hann ákveður því að búa
til forrit sem les inn upphaflegu töluna sem notuð var til að búa til
óendanlega stóru töluna, og svo tvær heiltölur `i` og `j`. Forritið á svo að
skrifa út alla tölustafina frá tölustafi númer `i` í tölunni til tölustafs
númer `j` í tölunni.

En þá allt í einu fattar Jón litli að hann kann ekki að forrita! Hann biður þig
því um aðstoð.

Ef við tökum sem dæmi óendanlega stóra töluna sem búin er til með tölunni
`6883`, og við viljum fá bútinn af tölunni frá `i = 3` og upp að `j = 7`, þá
mun forritið skila `83688`. Búturinn er undirstrikaður í tölunni að ofan.

## Inntak

Á fyrstu línu er heiltalan <code>1 &leq; T &leq; 100</code>, sem táknar fjölda
prófunartilvika sem fylgja. Hvert prófunartilvik samanstendur af tveimur línum.

Á fyrri línunni eru heiltölurnar `i` og `j`, aðskildar með bili, þar sem
<code>1 &leq; i &leq; j &leq; 10<sup>9</sup></code> og <code>j - i <
10<sup>4</sup></code>.

Á seinni línunni er talan sem notuð var til að búa til óendanlega stóru töluna.
Athuga skal að þessi tala getur verið allt að 100 tölustafir að lengd, en hefur
að minnsta kosti einn tölustaf.

## Úttak

Skrifa skal út eina línu með bútinum af óendanlega stóru tölunni frá tölustafi
númer `i` til tölustafs númer `j`. Athuga skal að fyrsti tölustafurinn er númer
`1`, annar tölustafurinn númer `2`, og svo framvegis.

