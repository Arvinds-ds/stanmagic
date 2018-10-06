/**
 * Enable highlighting of matching words in cells' CodeMirror editors.
 *
 * This extension was adapted from the CodeMirror addon
 * codemirror/addon/search/match-highlighter.js
 */

define(function (require, exports, module) {
	'use strict';

    var themes = {
      "Default": null,
      "stan": "./stan.css",
    };


	var $ = require('jquery');
	var Jupyter = require('base/js/namespace');
	var Cell = require('notebook/js/cell').Cell;
	var CodeCell = require('notebook/js/codecell').CodeCell;

	var CodeMirror = require('codemirror/lib/codemirror');

	require('codemirror/addon/selection/mark-selection');
	var stan = require(['./stan']);
    //require('codemirror/addon/selection/anyword-hint');
    //require('codemirror/addon/selection/show-hint');

	var globalState = {
		active: false,
		timeout: null, // only want one timeout
		overlay: null, // one overlay suffices, as all cells use the same one
	};

	// define a CodeMirror option for highlighting matches in all cells
	CodeMirror.defineOption("syntaxhighlight", false, function (cm, val, old) {
		if (old && old != CodeMirror.Init) {
			globalState.active = false;
			clearTimeout(globalState.timeout);
			globalState.timeout = null;
			m.off("focus", callbackOnFocus);
			cm.off("blur", callbackOnBlur);
			cm.off("viewportChange", callbackViewportChange);
			cm.off("change", callbackOnChange);
			cm.off("cursorActivity", callbackCursorActivity);
		}
		if (val) {

			cm.on("focus", callbackOnFocus);
			cm.on("blur", callbackOnBlur);
			cm.on("viewportChange", callbackViewportChange);
			cm.on("change", callbackOnChange);
			cm.on("cursorActivity", callbackCursorActivity);

		}
	});


	function callbackOnChange (cm) {
		scheduleHighlight(cm);

	}

	function callbackCursorActivity (cm) {
		scheduleHighlight(cm);

	}

	function callbackViewportChange (cm) {
		scheduleHighlight(cm);

	}
	function callbackOnFocus (cm) {
		scheduleHighlight(cm);
	}

	function callbackOnBlur (cm) {
		scheduleHighlight(cm);
	}


	function scheduleHighlight (cm) {

		highlightMatchesInAllRelevantCells(cm);
	}

	/**
	 *  Adapted from cm match-highlighter's highlightMatches, but adapted to
	 *  use our global state and parameters, plus work either for only the
	 *  current editor, or multiple cells' editors.
	 */
	function highlightMatchesInAllRelevantCells (cm) {
		get_relevant_cells().forEach(function (cell, idx, array) {
		    cell.code_mirror.setOption('mode', 'text/x-stan');
		    cell.code_mirror.setOption('theme', "stan");
		    cell.code_mirror.setOption('firstLineNumber',0);
		    cell.code_mirror.setOption('lineNumbers',true);
            cell.code_mirror.setOption('indentUnit',2);
            cell.code_mirror.setOption('smartIndent',true);

		});

    }

	function get_relevant_cells () {
		var cells = Jupyter.notebook.get_cells();
		var relevant_cells = [];
		for (var ii=0; ii<cells.length; ii++) {
			var cell = cells[ii];
			if ( cell.get_text().match("^%%stan") && cell instanceof CodeCell) {
				relevant_cells.push(cell);
			}
		}
		return relevant_cells;
	}

	function update_options () {
		get_relevant_cells().forEach(function (cell, idx, array) {
					cell.code_mirror.setOption('mode', 'text/x-stan');
                    cell.code_mirror.setOption('theme', "stan");
					cell.code_mirror.setOption('firstLineNumber',0);
                    cell.code_mirror.setOption('lineNumbers',true);
                    cell.code_mirror.setOption('indentUnit',2);
                    cell.code_mirror.setOption('smartIndent',true);
				});

    }

    function load_css(theme) {
        // Create a link element to attach the styles
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = require.toUrl(themes[theme]);
        link.id = theme + "-css";
        document.getElementsByTagName("head")[0].appendChild(link);
    }

    function load_font(href) {
      // Create a link element to attach the font
      var link = document.createElement("link");
      link.type = "text/css";
      link.rel = "stylesheet";
      link.href = href;
      document.getElementsByTagName("head")[0].appendChild(link);
    }


	function load_extension () {
		console.log("stan_code_helper loaded..")
		Jupyter.notebook.config.loaded
        .then(update_options, function on_error (reason) {
            console.warn('[stan]', 'error loading config:', reason);
        })
        .then(function () {
            // Apply to any already-existing cells
            var cells = Jupyter.notebook.get_cells().forEach(function (cell) {
                if ( cell instanceof CodeCell) {
                    cell.code_mirror.setOption('syntaxhighlight', true);
                    if (cell.get_text().match("^%%stan")) {
                        load_css("stan")
                        cell.code_mirror.setOption('mode', 'text/x-stan');
                    }

                }
            });
        })
        .catch(function on_error (reason) {
            console.warn('[stan]', 'error:', reason);
        });
		Jupyter.notebook.events.on('create.Cell', function(evt, data) {
                // data.cell is the cell object
                //notebook_cell = data.cell;
                console.log('EXTENSION: creating a cell');
                var cells = Jupyter.notebook.get_cells().forEach(function (cell) {
                if ( cell instanceof CodeCell) {
                    cell.code_mirror.setOption('syntaxhighlight', true);
                    load_css("stan")
                }
            });
        });

		Jupyter.notebook.events.on('execute.CodeCell', function(evt, data) {
                // data.cell is the cell object
                //notebook_cell = data.cell;
                console.log('EXTENSION: executing a cell');
                var cells = Jupyter.notebook.get_cells().forEach(function (cell) {
                if ( cell instanceof CodeCell) {
                    cell.code_mirror.setOption('syntaxhighlight', true);
                    if (cell.get_text().match("^%%stan")) {
                        cell.code_mirror.setOption('mode', 'text/x-stan');
                    }
                }
            });
        });

		Jupyter.notebook.events.on('select.Cell', function(evt, data) {
                // data.cell is the cell object
                //notebook_cell = data.cell;
                console.log('EXTENSION: selecting a cell');
                var cells = Jupyter.notebook.get_cells().forEach(function (cell) {
                if ( cell instanceof CodeCell ) {
                    cell.code_mirror.setOption('syntaxhighlight', true);
                    if (cell.get_text().match("^%%stan")) {
                        cell.code_mirror.setOption('mode', 'text/x-stan');
                    }
                }
            });
        });

	}

	return {
		load_ipython_extension : load_extension
	};
});
