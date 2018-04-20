const deviceId = 0;
const deviceTableRow = '<tr>\
  <th scope="row">__index__</th> \
  <td>__name__</td> \
  <td>__status__</td> \
  <td>OK</td> \
  <td><button type="button" class="btn btn-outline-info btn-sm mb-1" data-toggle="modal" data-target="#deviceDetailsModal" onclick="setSelectedDevice(__pk__)">Ver más </button></td> \
</tr>'

const populateDeviceInfo = (device) => {
  jQuery('#detail_deviceId').text(device.fields.unique_id)
  jQuery('#detail_deviceName').text(device.fields.name)
}

const populateDeviceSchedule = (schedule) => {
  const $ = jQuery
  const timing = [
    'hour',
    'minute',
    'am_pm'
  ]
  const days = [
    'on_monday',
    'on_tuesday',
    'on_wednesday',
    'on_thursday',
    'on_friday',
    'on_saturday',
    'on_sunday'
  ]
  days.forEach(day => $(`input[name=${day}]`)[0].checked=schedule.fields[day] === true)
  timing.forEach(time => $(`select[name=${time}]`).val(schedule.fields[time]))
}

const setSelectedDevice = (deviceId) => {
  jQuery('#detail_id').val(deviceId)

  if (deviceId === '') return

  getDevice(deviceId)
  .done((data) => {
    const [device] = JSON.parse(data)
    populateDeviceInfo(device)
  })
  .fail(() => alert('Could not get the device'))

  getDeviceSchedule(deviceId)
  .done(data => {
    const [schedule] = JSON.parse(data)
    populateDeviceSchedule(schedule)
  })
  .fail(() => jQuery( ':reset' ).click())
}

const createDevice = (event) => {
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

const getDevice = (deviceId) => {
  const $ = jQuery
  return $.ajax({
    url: `/api/devices/${deviceId}`,
    method: "GET",
    accepts: { 'Content-Type': 'application/json' },
  })
}

const deviceScheduleUrl = (deviceId) => `/api/devices/${deviceId}/schedule`

const getDeviceSchedule = (deviceId) => {
  const $ = jQuery
  const url = deviceScheduleUrl(deviceId)
  return $.ajax({
    url,
    method: "GET",
    accepts: { 'Content-Type': 'application/json' },
  })
}

const scheduleDevice = (event) => {
  event.preventDefault()

  const $ = jQuery
  const deviceId = $('#detail_id').val()
  const scheduleDeviceForm = $("#scheduleDeviceForm").serialize()

  return $.ajax({
    url: `/api/devices/${deviceId}/schedule`,
    method: "POST",
    accepts: { 'Content-Type': 'application/json' },
    data: scheduleDeviceForm
  }).done(function(data) {
    setSelectedDevice('')
    $('#deviceDetailsModal').click()
    $( ':reset' ).click()
  }).fail(() => alert('Could not update the device'))
}
