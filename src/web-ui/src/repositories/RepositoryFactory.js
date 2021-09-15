// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import ProductsRepository from "./productsRepository.js"
import UsersRepository from "./usersRepository.js"
import RecommendationsRepository from "./recommendationsRepository.js"

const repositories = {
    products: ProductsRepository,
    users: UsersRepository,
    recommendations: RecommendationsRepository,
}

export const RepositoryFactory = {
    get: name => repositories[name]
}