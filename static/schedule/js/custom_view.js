import {sliceEvents, createPlugin} from "https://cdn.jsdelivr.net/npm/@fullcalendar/core@6.1.9/+esm";

const CustomViewConfig = {

classNames: [ 'custom-view' ],

content: function(props) {
    let segs = sliceEvents(props, true); // allDay=true
    let html =
      '<div class="view-title">' +
        props.dateProfile.currentRange.start.toUTCString() +
      '</div>' +
      '<div class="view-events">' +
        segs.length + ' events' +
      '</div>'

    return { html: html }
  }

}

const customViewPlugin = createPlugin({
  views: {
    custom: CustomViewConfig
  }
});

export default customViewPlugin