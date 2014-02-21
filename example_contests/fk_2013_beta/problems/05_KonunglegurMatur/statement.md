<p>Hvíti kóngurinn og hvíta drottningin í skáklandi voru að fara að undirbúa kvöldmáltíðina þegar þau taka eftir því að það vantar sósu til að hafa með matnum. Venjulega myndu þau láta riddara skreppa út í búð fyrir sig, en báðir hvítu riddararnir eru í bardaga við svörtu riddarana, og því ekki heima. Kóngurinn og drottningin ákveða því að annaðhvort þeirra fer út í búð á meðan sá sem bíður heima leggur á borðið. En þau eru bæði orðin mjög svöng, þannig þau vilja að sá sem er fljótari að fara út í búð fari.</p>

<p>Skákland er í rauninni bara skákborð af stærð <tt>N &times; N</tt>. Konungsfjölskyldan er staðsett á reitnum <tt>(s<sub>r</sub>, s<sub>c</sub>)</tt>, á meðan búðin er staðsett á reitnum <tt>(t<sub>r</sub>, t<sub>c</sub>)</tt>. Þegar kóngurinn og drottningin eru að ferðast, þá taka þau skref. Í einu skrefi getur kóngurinn farið einn áfram í hvaða átt sem er (og þá eru áttirnar á ská líka teknar með), á meðan að drottningin getur í einu skrefið farið eins marga áfram og hún vill í hvaða átt sem er (og þá eru áttirnar á ská líka teknar með). Athuga skal að þessi skref eru alveg eins í hefðbundinni skák fyrir kóng og drottningu. Líka skal athuga að hvorki kóngurinn né drottningin mega fara úr skáklandi þegar þau eru að taka skref.</p>

<p>Skrifið forrit sem les inn <tt>N</tt>, <tt>t<sub>r</sub></tt>, <tt>t<sub>c</sub></tt>, <tt>s<sub>r</sub></tt> og <tt>s<sub>c</sub></tt>, og skrifar út hver þarf færri skref til að komast út í búð, og lætur vita ef skrefafjöldi er sá sami fyrir bæði kónginn og drottninguna.</p>

<h2>Inntak</h2>
<p>Á fyrstu línu er heiltalan <tt>1 &leq; T &leq; 100</tt>, sem táknar fjölda prófunartilvika sem fylgja. Hvert prófunartilvik samanstendur af einni línu með heiltölunum <tt>1 &leq; N &leq; 1000000, 1 &leq; t<sub>r</sub>, t<sub>c</sub>, s<sub>r</sub>, s<sub>c</sub> &leq; N</tt>.</p>

<h2>Úttak</h2>

<p>Fyrir hvert prófunartilvik á að skrifa út eina línu sem inniheldur &ldquo;<tt>King</tt>&rdquo; ef kóngurinn þarf færri skref til að komast út í búð, &ldquo;<tt>Queen</tt>&rdquo; ef drottningin þarf færri skref til að komast út í búð, en &ldquo;<tt>Same</tt>&rdquo; ef drottningin og kóngurinn þurfa jafn mörg skref til að komast út í búð.</p>

