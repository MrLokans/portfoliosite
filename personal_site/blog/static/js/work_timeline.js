$(document).ready(function(){
  var container = document.getElementById('work-timeline');

  // Create a DataSet (allows two way data-binding)
  var items = new vis.DataSet([
    {
      id: 1,
      content: 'Gymnasium #42',
      start: '2013-05-16',
      end: '2014-06-16'
    },

    {
      id: 2, 
      content: 'VPI Photonics', 
      start: '2014-07-16', 
      end: new Date()
    },
  ]);

  // Configuration for the Timeline
  var options = {};

  // Create a Timeline
  var timeline = new vis.Timeline(container, items, options);
});

