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
     * @param batchOffset
     * @param qtyBatches
     * @returns RepliesResponse Successful Response
     * @throws ApiError
     */
    public static getReplies(
        batchOffset?: number,
        qtyBatches: number = 2,
    ): CancelablePromise<RepliesResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/replies',
            query: {
                'batch_offset': batchOffset,
                'qty_batches': qtyBatches,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
