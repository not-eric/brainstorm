const { Midi } = require('@tonejs/midi');
const midi = new Midi();

// parse file
function parseFile(file){
  //read the file
  const reader = new FileReader();
  reader.onload = function (e) {
    // load a midi file in the browser
    midi = await Midi.fromUrl("/brainstorm generator");
    midi = JSON.stringify(midi, undefined, 2);
  };
  reader.readAsArrayBuffer(file);
}