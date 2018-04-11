const deviceId = 0;
const deviceTableRow = '<tr>\
  <th scope="row">__index__</th> \
  <td>__name__</td> \
  <td>__status__</td> \
  <td>OK</td> \
  <td><button type="button" class="btn btn-outline-info btn-sm mb-1" data-toggle="modal" data-target="#deviceDetailsModal" onclick="setSelectedDevice(__pk__)">Ver más </button></td> \
</tr>'

function setSelectedDevice (deviceId) {
  jQuery('#detail_id').val(deviceId)

  if (deviceId === '') return

  getDevice(deviceId)
  .done((data) => {console.log('deviceIfo', data)})
  .fail(() => alert('Could not get the device'))
}

function createDevice(event) {
  const $ = jQuery
  const createDeviceForm = $("#createDeviceForm").serialize()
  event.preventDefault()
  // var name = $('#deviceName').val();
  $.ajax({
    method: "POST",
    // dataType: 'json',
    accepts: { 'Content-Type': "application/json" },
    data: createDeviceForm
  }).done(function(data) {
    $('#deviceName').val('');
    $("#addNewModal").click();
    const [{pk, fields}, ] = JSON.parse(data)
    $('#device_list > tbody:last-child')
    .append(deviceTableRow
      .replace('__index__', $('#device_list > tbody tr').length+1)
      .replace('__name__', fields.name)
      .replace('__status__', fields.status === 'act' ? 'active' : 'disabled')
      .replace('__pk__', pk)
    );

    setSelectedDevice(pk)
    $('#deviceDetailsModal').modal()
  }).fail(() => alert('Could not create the device'))
}

function getDevice(deviceId) {
  const $ = jQuery
  return $.ajax({
    url: `/dashboard/devices/${deviceId}`,
    method: "GET",
    accepts: { 'Content-Type': 'application/json' },
  })
}

function scheduleDevice(event) {
  event.preventDefault()

  const $ = jQuery
  const deviceId = $('#detail_id').val()
  const scheduleDeviceForm = $("#scheduleDeviceForm").serialize()
  console.log(scheduleDeviceForm)

  return $.ajax({
    url: `/dashboard/devices/${deviceId}/schedule`,
    method: "POST",
    accepts: { 'Content-Type': 'application/json' },
    data: scheduleDeviceForm
  }).done(function(data) {
    console.log(data)
    setSelectedDevice('')
    $('#deviceDetailsModal').click()
    $( ':reset' ).click()
  }).fail(() => alert('Could not update the device'))
}
