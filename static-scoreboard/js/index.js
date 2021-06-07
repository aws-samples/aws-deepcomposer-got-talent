// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

$(document).ready(function() {

  var dataSet = [];
    $.get('<your API gateway endpoint>', function(data) {
      console.log(data)
      for (i = 0; i < data.length; i++) {
        dataSet.push([[i+1], data[i][0], data[i][1]])
        console.log(data[i])
        
      }
      $('#m_table_1').DataTable( {
        "fnDrawCallback": function ( oSettings ) {
          /* Need to redo the counters if filtered or sorted */
          if ( oSettings.bSorted || oSettings.bFiltered )
          {
            
          }
      },
      "aoColumnDefs": [
          { "bSortable": false, "aTargets": [ 0, 1 ] }
      ],
      createdRow: function (row, data, index) {
          //
          // if the second column cell is blank apply special formatting
          //
          if (data[0] == "1") {
              //console.dir(row);
              $(row).addClass('first-place');
          }

          if (data[0] == "2") {
              //console.dir(row);
              $(row).addClass('second-place');
          }
          
          if (data[0] == "3") {
            //console.dir(row);
            $(row).addClass('third-place');
        }
      },
        info: false,
        paging: false,
        searching: true,
        ordering: true,
        data: dataSet,
        columns: [
            { title: "Rank" },
            { title: "Competitor" },
            { title: "Points" }
        ]
    } );
    })  
    
  
    
} );
