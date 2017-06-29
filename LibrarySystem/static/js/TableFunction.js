/* tables */
/* jQuery DataTables 插件简述 */
/* 
	参考网址 
	1. jQuery dataTables 的使用   http://blog.csdn.net/cdefg198/article/details/7182341
*/
/*
	--
		_fnCompatMap( init, 'ordering',      'bSort' );
		_fnCompatMap( init, 'orderMulti',    'bSortMulti' );
		_fnCompatMap( init, 'orderClasses',  'bSortClasses' );
		_fnCompatMap( init, 'orderCellsTop', 'bSortCellsTop' );
		_fnCompatMap( init, 'order',         'aaSorting' );
		_fnCompatMap( init, 'orderFixed',    'aaSortingFixed' );
		_fnCompatMap( init, 'paging',        'bPaginate' );
		_fnCompatMap( init, 'pagingType',    'sPaginationType' );
		_fnCompatMap( init, 'pageLength',    'iDisplayLength' );
		_fnCompatMap( init, 'searching',     'bFilter' );

	-- 参考网址：http://www.drayge.com/pages/8196.html
	1. 禁用排序功能："ordering": false
	2. 禁用分页功能："bPaginate": false
	3. 设置分页页数："lengthMenu": [100, 200, 300]
	4. 设置默认分页页数："iDisplayLength": 10
	5. 禁用搜索过滤功能："bFilter": false
*/

// 配置dataTable
$(document).ready( function () {
    var uisearch_QuestionList = $('#sb-search');
    var DataTable_QuestionList = $('#DataTable_QuestionList').DataTable({
      "ordering": false,
      "bDestroy": true,
      "retrieve": true,
	    "bPaginate": true,
      "iDisplayLength": 25,
      "language": {
      "paginate": {
          "sNext": "下一页",
          "sPrevious": "上一页",
        },
        "loadingRecords": "正在加载中.....",
        "zeroRecords": "对不起，查询不到相关数据！",
        "infoFiltered": "【从 _MAX_ 条数据中搜索的结果】"
      },
      "search": {"search": ""},
      //"sSearch": "搜索",
      "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0
        } ],
        "order": [[ 1, 'asc' ]],
        "bLengthChange": false,
        
    });

    // 在第1列显示从1开始的序号
    /*
    DataTable_QuestionList.on( 'order.dt search.dt', function () {
      DataTable_QuestionList.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
          cell.innerHTML = i+1;
      } );
    } ).draw();*/

    // 控制“显示或隐藏列的按钮”
    $('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();

        // Get the column API object
        var column = DataTable_QuestionList.column( $(this).attr('data-column') );
        // Toggle the visibility
        column.visible( ! column.visible() );
    } );


  // Download area
  var DataTable_DownloadArea = $('#DataTable_DownloadArea').DataTable({
    "ordering":false,
    "lengthMenu": [5, 10, 15, 20, 30],
  });

  // 在第1列显示从1开始的序号
  /**/
  DataTable_DownloadArea.on( 'order.dt search.dt', function () {
    DataTable_DownloadArea.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
        cell.innerHTML = i+1;
    } );
  } ).draw();


  // 预约模块

});