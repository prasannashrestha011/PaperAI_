"use client"
import React, { useEffect } from 'react'
import DocViewResizeable from './ResizeableTab'
import { useUserStore } from '@/store/userStore'
import PdfViewer from './PdfViewer'
import { docService } from '@/services/docService'
import { useQuery } from '@tanstack/react-query'

const SessionView = ({ doc_id }: { doc_id: string }) => {
  const { user } = useUserStore()

  const hasUser = !!user?.user_id

  const { data: doc, isLoading, error } = useQuery({
    queryKey: ['doc',doc_id],
    queryFn: () => docService.getDocInfo( doc_id),
    enabled: hasUser && !!doc_id,
    staleTime: 1000 * 60 * 5,
  })

  useEffect(()=>{console.log(doc)},[doc])
  if (!hasUser) {
    return <div>Session expired, login again</div>
  }

  if (isLoading) {
    return <div>Loading doc.</div>
  }

  if (error) {
    return <div>Failed to load the doc</div>
  }

  return (
    <div>
      <PdfViewer userID={user.user_id} docID={doc_id} filename={doc?.file_name!} />
    </div>
  )
}

export default SessionView
