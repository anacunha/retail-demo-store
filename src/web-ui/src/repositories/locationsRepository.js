// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

// import axios from "axios";

// const serviceDomain = process.env.VUE_APP_PRODUCTS_SERVICE_DOMAIN;
// const servicePort = process.env.VUE_APP_PRODUCTS_SERVICE_PORT;
// const baseURL = `${serviceDomain}:${servicePort}`;

// const connection = axios.create({
//     baseURL
// })

// const resource = "/locations";
export default {
    get() {
        // return connection.get(`${resource}/all`)
        return [
            {
                id: 1,
                name: 'Surly Brewing Co',
                latitude: '44.973270',
                longitude: '-93.210838',
                address: '520 Malcolm Ave SE<br/>Minneapolis, MN 55414',
                hours: 'Sunday - Monday Closed<br/>Tuesday - Saturday 3PM-11PM'
            },
            {
                id: 2,
                name: 'Sociable Cider Werks',
                latitude: '45.002790',
                longitude: '-93.242330',
                address: '1500 Fillmore St NE<br/>Minneapolis, MN 55413',
                hours: 'Sunday - Thursday 12PM-11PM<br/>Friday - Saturday 12PM-12AM'
            },
            {
                id: 3,
                name: 'Three Sheets Craft Beer Bar',
                latitude: '36.158080',
                longitude: '-115.151930',
                address: '1115 S Casino Center Blvd<br/>Las Vegas, NV 89104',
                hours: 'Monday - Closed<br/>Tuesday - Closed<br/>Wednesday - 4pm - 11pm<br/>Thursday 4pm - 11pm<br/>Friday - 1pm - 12am<br/>Saturday - 12pm - 12am<br/>Sunday - 12pm - 7pm'
            }
        ]
    },
    // getLocation(locationID) {
    //     // if (!productID || productID.length == 0)
    //     //     throw "productID required"
    //     // return connection.get(`${resource}/id/${productID}`)
    //     return {
    //         id: 1,
    //         name: 'Surly Brewing Co',
    //         latitude: '44.973270',
    //         longitude: '-93.210838',
    //         address: '520 Malcolm Ave SE, Minneapolis, MN 55414',
    //         hours: 'Closed Sunday - Monday; 3PM-11PM Tuesday - Saturday'
    //     }
    // }
}