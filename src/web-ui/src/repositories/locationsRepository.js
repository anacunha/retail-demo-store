// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import axios from "axios";

const serviceDomain = process.env.VUE_APP_LOCATION_SERVICE_DOMAIN;
const servicePort = process.env.VUE_APP_LOCATION_SERVICE_PORT;

const baseURL = `${serviceDomain}:${servicePort}`;

const connection = axios.create({
    baseURL
})

const resource = "/locations";
export default {
    get() {
        return connection.get(`${resource}/all`)
    },

    getLocationsByBeer(beerName) {
        return connection.get(`${resource}?beerName=${beerName}`)
    }
}