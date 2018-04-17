$(document).ready(function(){

  var container = document.getElementById('work-timeline');

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
      end: '2016-07-16'
    },
    {
      id: 3,
      content: 'itransition',
      start: '2016-07-18',
      end: new Date()
    }
  ]);

  // Configuration for the Timeline
  var options = {};

  // Create a Timeline
  var timeline = new vis.Timeline(container, items, options);
});

