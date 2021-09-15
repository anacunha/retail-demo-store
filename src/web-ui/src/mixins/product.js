// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { mapState } from 'vuex';

import { RepositoryFactory } from '@/repositories/RepositoryFactory';
import { capitalize } from '@/util/capitalize';
import { getProductImageUrl } from '../util/getProductImageUrl';

const ProductsRepository = RepositoryFactory.get('products');

export const product = {
  data() {
    return {
      product: null,
    };
  },
  computed: {
    ...mapState(['user']),
    productImageUrl() {
      if (!this.product) return null;

      return getProductImageUrl(this.product);
    },
    readableProductCategory() {
      if (!this.product) return null;

      return capitalize(this.product.category);
    },
  },
  methods: {
    async getProductByID(product_id) {
      const { data } = await ProductsRepository.getProduct(product_id);
      this.product = data;
    },
  },
};
