/* ------------------------------------------------------------------------------
*
*  # Datatables data sources
*
*  Specific JS code additions for datatable_data_sources.html page
*
*  Version: 1.0
*  Latest update: Aug 1, 2015
*
* ---------------------------------------------------------------------------- */
$(function () {
    $(document).ready(function () {
        console.log($('.frAdmin-datatable').data('url'));
        $('.frAdmin-datatable').each(function () {
            
        }).DataTable({
            ajax: $(this).data('url')
        });
    });
});
