/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RepliesResponse } from '../models/RepliesResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class RepliesService {
    /**
     * Get Replies
     * @param page
     * @param items
     * @returns RepliesResponse Successful Response
     * @throws ApiError
     */
    public static getReplies(
        page: number = 1,
        items: number = 10,
    ): CancelablePromise<RepliesResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/replies',
            query: {
                'page': page,
                'items': items,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
