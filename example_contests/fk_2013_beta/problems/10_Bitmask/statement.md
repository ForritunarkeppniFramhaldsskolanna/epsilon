
<p>Bitagrímur (eða <it>bitmasks</it>) koma oft upp þegar unnið er með bita og bitareikning. Með þessum grímum er hægt að fá fram allskonar bitamynstur. Til dæmis er hægt að núllstilla fyrstu fjóra bitana í 32-bita tölu með því að nota bitagrímuna <tt>0xFFFFFFF0</tt> og nota svo <tt>AND</tt> bitaaðgerðina. Í þessu dæmi átt þú að finna svona bitagrímu.</p>

<p>Þú færð gefnar þrjár 32-bita jákvæðar heiltölu <tt>N</tt>, <tt>L</tt> og <tt>U</tt>. Þú átt að finna bitagrímu <tt>M</tt> þannig að <tt>L &leq; M &leq; U</tt> og <tt>N OR M</tt> er í hámarki. Til dæmis ef <tt>N</tt> er 100, og <tt>L = 50</tt>, <tt>U = 60</tt>, þá mun <tt>M</tt> vera <tt>59</tt> og <tt>N OR M</tt> mun vera <tt>127</tt>, sem er í hámarki. Ef fleiri en eitt gildi fyrir <tt>M</tt> uppfylla þessi skilyrði, þá skaltu nota minnsta gildið.</p>

<h2>Inntak</h2>

<p>Á fyrstu línu er heiltalan <tt>1 &leq; T &leq; 1000</tt>, sem táknar fjölda prófunartilvika sem fylgja. Hvert prófunartilvik samanstendur af einni línu með þremur 32-bita jákvæðum heiltölum <tt>N</tt>, <tt>L</tt> og <tt>U</tt>, þar sem <tt>L &leq; U</tt>.</p>

<h2>Úttak</h2>

<p>Fyrir hvert prófunartilvik á að skrifa út minnsta gildi fyrir <tt>M</tt> þannig að <tt>N OR M</tt> er í hámarki.</p>

