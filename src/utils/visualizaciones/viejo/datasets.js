var dataset3 = {
   "datasets":['dataset1', 'dataset2', 'dataset3'],
   "datasets_nodes":[
      {"name":"dataset1", "id":"dataset1", "level": "coupled", "color": "blue"}, 
      {"name":"dataset2", "id":"dataset2", "level": "coupled", "color": "blue"},
      {"name":"dataset3", "id":"dataset3", "level": "coupled", "color": "blue"}
   ],
   "datasets_links":[
      {"source":"dataset1", "target":"dataset2"},
      {"source":"dataset3", "target":"dataset2"}
   ],

   "dataset1": {
      "datasets":[],
      "nodes":[
         {"name":"Abc", "id":"1", "level":"atomic", "color": "red"}, {"name":"Aaa", "id":"2", "level":"atomic", "color": "red"}
      ],
      "links":[
         {"source":"1", "target":"2"}
      ],
      "datasets_nodes":[],
      "datasets_links":[]
   },

   "dataset2": {
      "datasets":[],
      "nodes":[
         {"name":"Abc", "id":"1", "level":"atomic", "color": "red"}, 
         {"name":"Aaa", "id":"2", "level":"atomic", "color": "red"}, 
         {"name":"JTY", "id":"3", "level":"atomic", "color": "red"},
         {"name":"ZZZ", "id":"4", "level":"atomic", "color": "red"}
      ],
      "links":[
         {"source":"1", "target":"2"}, 
         {"source":"3", "target":"2"},
         {"source":"2", "target":"4"}
      ]
   },

   "dataset3": {
      "datasets":['sub-dataset-1', 'sub-dataset-2'],
      "datasets_nodes":[
         {"name":"sub-dataset-1", "id":"sub-dataset-1","level":"coupled","color":"blue"},
         {"name":"sub-dataset-2", "id":"sub-dataset-2","level":"coupled","color":"blue"}
      ],
      "datasets_links":[
         {"source":"sub-dataset-1", "target":"sub-dataset-2"}
      ],

      'sub-dataset-1': {
         "datasets":['sub-sub-dataset-1', 'sub-sub-dataset-2'], 
         
         "datasets_nodes": [{"name":"sub-sub-dataset-1", "id":"sub-sub-dataset-1","level":"coupled","color":"blue"},{"name":"sub-sub-dataset-2", "id":"sub-sub-dataset-2","level":"coupled","color":"blue"}],
         "datasets_links": [],
         'sub-sub-dataset-1': {"datasets":[], 
            "nodes": [{"name":"A", "id":"A", "level":"atomic", "color": "red"}, {"name":"B", "id":"B", "level":"atomic", "color": "red"}], 
            "links":[{"source":"A", "target":"B"}]},
         'sub-sub-dataset-2': {"datasets":[], 
            "nodes": [{"name":"A", "id":"A", "level":"atomic", "color": "red"}], 
            "links":[]}
      },
      'sub-dataset-2': {
         "datasets":['sub-sub-dataset-3', 'sub-sub-datset-4'],
         "datasets_nodes": [{"name":"sub-sub-dataset-3", "id":"sub-sub-dataset-3","level":"coupled","color":"blue"},{"name":"sub-sub-dataset-4", "id":"sub-sub-dataset-4","level":"coupled","color":"blue"}],
         "datasets_links": [],
         'sub-sub-dataset-3': {"datasets":[], "nodes": [{"name":"A", "id":"A", "level":"atomic", "color": "red"}], "links":[]},
         'sub-sub-datset-4': {"datasets":[], "nodes": [{"name":"A", "id":"A", "level":"atomic", "color": "red"}], "links":[]}
      },
   }
}

var dataset1 = {
   "datasets":[],
   "nodes":[  
      {  
         "name":"Abc",
         "id":"1",
      },
      {  
         "name":"Aaa",
         "id":"2",
      },
      {  
         "name":"JTY",
         "id":"3",
      },
      {  
         "name":"TTT",
         "id":"4",
      },
      {  
         "name":"MMM",
         "id":"5",
      }
   ],
   "links":[  
      {  
         "source":"2",
         "target":"1"
      },
      {  
         "source":"3",
         "target":"1"
      },
      {  
         "source":"1",
         "target":"4"
      },
      {
        "source":"5",
        "target":"2"
      }
   ]
};
var dataset2 = {
   "datasets":[],
   "nodes":[  
      {  
         "name":"Abc",
         "id":"1",
      },
      {  
         "name":"Aaa",
         "id":"2",
      },
      {  
         "name":"JTY",
         "id":"3",
      },
      {  
         "name":"TTT",
         "id":"4",
      },
      {  
         "name":"MMM",
         "id":"5",
      }
   ],
   "links":[  
      {  
         "source":"2",
         "target":"1"
      },
      {  
         "source":"3",
         "target":"1"
      },
      {  
         "source":"1",
         "target":"4"
      },
      {
        "source":"5",
        "target":"2"
      }
   ]
};