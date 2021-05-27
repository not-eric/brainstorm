const { Midi } = require('@tonejs/midi');
const midi = new Midi();

// parse file
function parseFile(file){
  // load a midi file in the browser
  midi = await Midi.fromUrl("/brainstorm generator");
  //read the file + convert
  const reader = new FileReader();
  reader.onload = function (midi) {
    midi = JSON.stringify(midi, undefined, 2);
  };
  reader.readAsArrayBuffer(file);
}