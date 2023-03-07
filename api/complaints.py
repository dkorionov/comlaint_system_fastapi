from typing import List

from fastapi import APIRouter, Request, Depends, Response

from managers.auth_manager import oauth2_scheme, is_complainer, is_admin, is_approver
from managers.complaint import ComplaintManager
from schemas.complaint import ComplaintOUT, ComplaintIN

router = APIRouter(tags=["complaints"])


@router.get("/", status_code=200, dependencies=[Depends(oauth2_scheme)], response_model=List[ComplaintOUT])
async def get_complaints(request: Request):
    return await ComplaintManager.get_complaints(request.state.user)


@router.post("/", status_code=201, dependencies=[Depends(oauth2_scheme), Depends(is_complainer)],
             response_model=ComplaintOUT)
async def create_complaint(complaint: ComplaintIN, request: Request):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


@router.delete("/{complaint_id}/", status_code=204, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete(complaint_id)
    return Response(status_code=204)


@router.put("/{complaint_id}/approve/", status_code=200, dependencies=[Depends(oauth2_scheme), Depends(is_approver)])
async def approve_complaint(complaint_id: int):
    await ComplaintManager.approve(complaint_id)
    return Response(status_code=200)


@router.put("/{complaint_id}/reject/", status_code=200, dependencies=[Depends(oauth2_scheme), Depends(is_approver)])
async def reject_complaint(complaint_id: int):
    await ComplaintManager.reject(complaint_id)
    return Response(status_code=200)
